import streamlit as st
from llama_index.core import VectorStoreIndex, ServiceContext, Document, SimpleDirectoryReader
from llama_index.llms.openai import OpenAI


# 1. Function to load and index data in your index_functions.py file
@st.cache_resource(show_spinner=True)  # Cache the data to avoid reloading every time
def load_data():
    # Spinner for user feedback while data is loading
    with st.spinner(text="Loading and indexing the data – hang tight! This shouldn't take more than a minute."):
        # Read documents from the directory and load them into memory
        reader = SimpleDirectoryReader(input_dir="./data", recursive=True)
        docs = reader.load_data()

        # Define the service context for the indexing, using GPT-3.5 Turbo model
        service_context = ServiceContext.from_defaults(
            llm=OpenAI(model="gpt-3.5-turbo", temperature=0.5,
                       system_prompt="You are an expert on the Innovation CoPilot and your job is to answer questions about it. Assume that all questions are related to the Innovation CoPilot. Keep your answers technical and based on facts – do not hallucinate features.")
        )
        # Create the index using the loaded documents and service context
        index = VectorStoreIndex.from_documents(docs, service_context=service_context)
        # Return the created index
        return index


# 2. This is how you would construct the index in the main.py file
# Call load_data function to get the indexed data
index = load_data()

# Create a chat engine using the indexed data; set the chat mode and verbosity (many options)
chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)


# 3. Example of how this index can be used in a generate_response function
def generate_response_index(prompt, history, model_name, temperature, chat_engine, last_user_message, full_prompt):
    # Initialize an empty string to store response fetched from the indexed data
    index_response = ""
    # Query the chat_engine using the last user message to get relevant data from indexed documents
    response = chat_engine.chat(last_user_message)
    # Store the relevant data fetched from indexed documents
    index_response = response.response
    # Append the relevant indexed data to the full_prompt to provide additional context to the chatbot
    full_prompt += f"\n### Relevant data from documents: {index_response}"