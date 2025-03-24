from langchain.prompts import MessagesPlaceholder, ChatPromptTemplate, PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableParallel
from langchain_community.chat_message_histories import ChatMessageHistory

import json

# Initialize a language model using OpenAI's GPT-4o-mini
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# Used to store and manage user and AI messages in memory.
# However, in production enviroment databases like Reddis need to be used.
# TODO Reddis for User Message history
chat_history = ChatMessageHistory()


class CoT:
    """
    A class to implement Chain of Thought (CoT) reasoning using LangChain's prompt templates and OpenAI's chat model.

    This class defines a system message that instructs the model to think step by step and structure its response
    in a specific format.
    """

    def __init__(self):
        self.history = chat_history  # Stores conversation history

        # System message guiding the model's reasoning process
        self.system_message = """Let's think step by step.
        Given the conversation below, break it down into smaller reasoning steps before arriving at the final answer.
        The answer should be strictly in the format below:
        Mark each step with the keyword 'Thought' and the actual answer with 'Final Response'"""

        # Define a chat prompt template with a system message and a placeholder for conversation history
        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", self.system_message),  # Instructional system message
                MessagesPlaceholder("history"),  # Placeholder for conversation history
            ]
        )

        # Create a processing chain by combining the prompt template with the language model
        self.chain = self.prompt_template | llm  # Pipeline: prompt → model

    def stream(self, message: str):
        """
        Streams the model's response in chunks.
        Extracts and stores only the final response in chat history.
        """

        self.history.add_user_message(message)  # Add user input to history

        response = ""
        for chunk in self.chain.stream({"history": self.history.messages}):
            chunk = chunk.content
            response += chunk
            yield chunk  # Stream response in real-time
        
        _, final = response.split("Final Response: ")  # Extract final response
        self.history.add_ai_message(final)  # Store final response in history



class CoTSC(CoT):
    """
    A class to implement Chain-of-Thought (CoT) reasoning with Self-Consistency (SC).

    This class defines a system message that instructs the model to reason step by step.
    It samples multiple responses and, in the final stage, selects the most consistent answer
    based on the majority or highest agreement among the generated outputs.
    """

    def __init__(self):
        super().__init__()  # Inherit CoT behavior so we can use CoT's chain

        # System message to aggregate multiple reasoning paths and determine the most consistent answer
        self.system_message = """
        Answer1: {cot0}
        Answer2: {cot1}
        Answer3: {cot2}
        Compare the conclusions from different reasoning paths and determine the most frequent or consistent final answer. 
        Just report the most robust solution with confidence.
        Final Answer: """

        self.prompt_template = PromptTemplate.from_template(self.system_message)  # Template for final answer selection

        # Run multiple CoT chains(Inherited from CoT class) in parallel to generate diverse reasoning outputs
        self.subchain = RunnableParallel({f"cot{i}": self.chain for i in range(3)})

        # Combine the aggregated responses with the final decision model
        self.chain = self.prompt_template | {"final": llm}

    def stream(self, message: str):
        """
        Streams multiple CoT responses, selects the most consistent answer, and stores it in history.
        """

        cots = {f"cot{i}": "" for i in range(3)}  # Initialize response storage
        self.history.add_user_message(message)  # Add user input to history

        # Stream responses from multiple reasoning paths
        for chunk in self.subchain.stream({"history": self.history.messages}):
            chunk = {k: v.content for k, v in chunk.items()}
            for k in chunk:
                cots[k] += chunk[k]  # Accumulate responses per path
            yield json.dumps(chunk) + "\n"  # Stream responses in JSON format

        final = ""
        # Stream final consistent answer
        for chunk in self.chain.stream(cots):
            chunk["final"] = chunk["final"].content
            final += chunk["final"]
            yield json.dumps(chunk) + "\n"  # Stream final answer in JSON format

        self.history.add_ai_message(final)  # Store final answer in history