from langchain.prompts import MessagesPlaceholder, ChatPromptTemplate
from langchain_openai import ChatOpenAI

# Initialize a language model using OpenAI's GPT-4o-mini
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

class CoT:
    """
    A class to implement Chain of Thought (CoT) reasoning using LangChain's prompt templates and OpenAI's chat model.
    
    This class defines a system message that instructs the model to think step by step and structure its response
    in a specific format.
    """
    
    # System message guiding the model's reasoning process
    system_message = """Let's think step by step.
    Given the conversation below, break it down into smaller reasoning steps before arriving at the final answer.
    The answer should be strictly in the format below:
    Mark each step with the keyword 'Thought' and the actual answer with 'Final Response'"""
    
    # Define a chat prompt template with a system message and a placeholder for conversation history
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_message),  # System message providing instructions
        MessagesPlaceholder("history")  # Placeholder for dynamic conversation history
    ])
    
    # Create a processing chain by combining the prompt template with the language model
    chain = prompt_template | llm
