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
        self.history = chat_history

        # System message guiding the model's reasoning process
        self.system_message = """Let's think step by step.
        Given the conversation below, break it down into smaller reasoning steps before arriving at the final answer.
        The answer should be strictly in the format below:
        Mark each step with the keyword 'Thought' and the actual answer with 'Final Response'"""

        # Define a chat prompt template with a system message and a placeholder for conversation history
        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", self.system_message),  # System message providing instructions
                MessagesPlaceholder(
                    "history"
                ),  # Placeholder for dynamic conversation history
            ]
        )

        # Create a processing chain by combining the prompt template with the language model
        self.chain = self.prompt_template | llm

    def stream(self, message: str):
        """
        Collects and streams the content from a generator (CoT engine's response stream).
        Once the final response is received,
        it splits the content to extract and store the AI's final response in the chat_history.
        and omits the thoughts part of response
        """

        self.history.add_user_message(message)

        response=""
        for chunk in self.chain.stream({"history": self.history.messages}):
            chunk = chunk.content
            response += chunk
            yield chunk
        
        _, final = response.split("Final Response: ")
        self.history.add_ai_message(final)



class CoTSC(CoT):
    """
    A class to implement Chain-of-Thought (CoT) reasoning with Self-Consistency (SC).

    This class defines a system message that instructs the model to reason step by step.
    It samples multiple responses and, in the final stage, selects the most consistent answer
    based on the majority or highest agreement among the generated outputs.
    """

    def __init__(self):
        super().__init__()

        self.system_message = """
        Answer1:{cot0}
        Answer2:{cot1}
        Answer3:{cot2}
        Compare the conclusions from different reasoning paths and determine the most frequent or consistent final answer. 
        Just report the most robust solution with confidence.
        Final Answer: """

        self.prompt_template = PromptTemplate.from_template(self.system_message)

        self.subchain = RunnableParallel({f"cot{i}": self.chain for i in range(3)})

        self.chain = self.prompt_template | {"final": llm}

    def stream(self, message: str):
        cots = {f"cot{i}": "" for i in range(3)}
        self.history.add_user_message(message)
        for chunk in self.subchain.stream({"history": self.history.messages}):
            chunk = {k: v.content for k, v in chunk.items()}
            for k in chunk:
                cots[k] = cots[k] + chunk[k]
            yield json.dumps(chunk) + "\n"

        final = ""
        for chunk in self.chain.stream(cots):
            chunk["final"] = chunk["final"].content
            final += chunk["final"]
            yield json.dumps(chunk) + "\n"

        self.history.add_ai_message(final)
