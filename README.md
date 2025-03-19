# Project Documentation

## Project Overview

### Project Name:
**State-of-the-Art Reasoning Chatbot System**

### Description:
This project explores and implements advanced reasoning techniques using GPT-4 Mini and LangChain to generate results based on multiple reasoning engines. It integrates these methods into a chatbot architecture, enabling users to interact with a system that performs complex reasoning tasks. The system is designed with a seamless interaction between the frontend (Streamlit) and backend (Django & DRF).

### Architecture Overview:
The system consists of two main components:
- **Frontend (Streamlit)**: A user-friendly interface where users can interact with the chatbot. Streamlit is used to build the interactive interface that sends messages to the backend and streams responses from the model.
- **Backend (Django & DRF)**: Handles the logic for processing messages, interacting with the LangChain-based reasoning engines, and generating responses using GPT-4 Mini. The backend also stores chat history and manages the state of conversations.

The reasoning engines used are:
- **CoT (Chain-of-Thought)**: A reasoning technique that breaks down tasks into smaller steps, allowing for structured reasoning and more detailed responses.
- **TOT (Tree-of-Thought)**: A variant of the Chain-of-Thought approach that uses tree-like structures to organize reasoning steps and improve complex decision-making. **Not Implemented**
- **CoT-SC (Chain-of-Thought with Self-Consistency)**: An extension of the Chain-of-Thought approach that checks for consistency in the reasoning process. It generates multiple reasoning paths and selects the most consistent one to improve the reliability of the final answer. **Not Implemented**

These reasoning engines are integrated into the system via LangChain, which facilitates the chaining of different reasoning components.


### Tech Stack:
- **Backend**: Django, Django REST Framework (DRF)
- **Frontend**: Streamlit
- **LLM Integration**: GPT-4 Mini (used for the language model and reasoning tasks)
- **Reasoning Framework**: LangChain (used for chaining and processing the reasoning steps)
  
### Key Features:
- **Reasoning-based Chatbot**: Uses advanced LLMs to reason through tasks and generate informed responses.
- **Interactive UI**: Streamlit provides a simple, real-time interface for users to interact with the model.
- **State Management**: Chat history is stored and used to improve responses based on previous messages.

## Installation and Setup

### Local Setup

#### Prerequisites:
- **Python**: Ensure you are using **Python 3.11**.
- **Libs**: Refer to the requirements.txt in each stack

#### Installation Steps:
- **Front-end**: pip install -r ./Front-end/requirements.txt
- **Back-end**: pip install -r ./Back-end/requirements.txt
- **Set Up Environment Variables**: Create a .env file in the Back-end/core directory and add your OpenAI API key as follows:
    OPENAI_API_KEY=<your_openai_api_key_here>

### Docker Setup
- **Not Implemented**

## API Usage

### History View
- **Endpoint**: `/chat/history/`
- **Method**: `GET`
- **Description**: Retrieves the entire chat history as a dictionary.

### Chain-of-Thought (CoT) View
- **Endpoint**: `/chat/cot/`
- **Method**: `GET`
- **Parameters**:
  - `message`: The user's message to process (passed as a query parameter).
- **Description**: Streams the response from the CoT engine as a generator function and adds both the user's message and AI's final response to the chat history.

## LLM Integration

### LLM Provider: 
**OpenAI**

### Model Used:
The model used is **GPT-4o Mini**. Other models like **Llama 3** and **Mistral** can be used as alternatives, depending on the specific use case or model preference.

### How Requests are Processed:
The request flow follows this sequence:
1. **Streamlit**: The user interacts with the frontend (Streamlit) which sends a request to the Django API.
2. **Django API**: The backend processes the request by sending it to the LLM service (e.g., GPT-4o Mini via OpenAI API).
3. **LLM Service**: The LLM generates a response which is sent back to the Django API.
4. **Response**: Then forwards it to the frontend.

### Streaming Response:
For real-time interactions, particularly for long or multi-step responses (e.g. Tree of Thoughts), the system supports **streaming responses**. This is achieved using:
**Streaming API**: Implemented via Django's `StreamingHttpResponse` to send incremental data as the LLM processes and returns the response.

This enables a smooth user experience, especially for longer or complex reasoning tasks.

## Database:
A SQL Database is needed for handeling django models. **Not Implemented**
An in memory storage is also needed for storing the user's chat history, Ideally `Redis`. **Not Implemented**

## Logging & Monitoring
Ideally `structlog` and `loguru` **Not Implemented**

# TODO:
- **Building Docker images for each service**
- **SQL Database**
- **In memory storage for Chat History**
- **Logger**
- **CoT-SC**
- **ToT**