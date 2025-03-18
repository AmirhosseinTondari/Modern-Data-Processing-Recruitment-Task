from langchain.prompts import MessagesPlaceholder, ChatPromptTemplate
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

class CoT:
    system_message = """Let's think step by step.
Given the conversation below, break it down into smaller reasoning steps before arriving at the final answer.
the answer should be strictly in format below
Mark each step with keyword 'Thought' and the actual answer with 'Final Response'"""

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_message),
        MessagesPlaceholder("history")
    ])

    chain = prompt_template | llm