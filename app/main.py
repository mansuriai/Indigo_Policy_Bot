# app/main.py
import streamlit as st
from pathlib import Path
import time
from typing import List, Dict
import os, sys
from urllib.parse import urlencode
from pinecone import Pinecone, ServerlessSpec

#################
# import sys
# sys.modules["sqlite3"] = __import__("pysqlite3")
####################


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# from utils.apikey import OPENAIAPI
from utils.config import config
os.environ["OPENAI_API_KEY"] = config.OPENAI_API_KEY

from utils.config import config

# Set page config as the first Streamlit command
st.set_page_config(
    page_title=config.APP_TITLE,
    layout="wide",
)

from core.embeddings import EmbeddingManager
from core.vector_store import VectorStore
from core.llm import LLMManager
from components.chat import render_chat_interface


###### pine cone changes ###################
# Add environment variables check
# def check_environment():
#     required_vars = [
#         "OPENAI_API_KEY",
#         "PINECONE_API_KEY",
#         "PINECONE_ENVIRONMENT"
#     ]
    
#     missing_vars = [var for var in required_vars if not os.getenv(var)]
    
#     if missing_vars:
#         st.error(f"Missing required environment variables: {', '.join(missing_vars)}")
#         st.stop()
    

###########################################

# Initialize components with error handling

## Old Working ##
# @st.cache_resource
# def initialize_components():
#     try:
#         return {
#             'embedding_manager': EmbeddingManager(),
#             'vector_store': VectorStore(),
#             'llm_manager': LLMManager()
#         }
#     except Exception as e:
#         st.error(f"Error initializing components: {str(e)}")
#         return None

def check_environment():
    """Check if all required environment variables are set."""
    missing_vars = []
    
    if not config.OPENAI_API_KEY:
        missing_vars.append("OPENAI_API_KEY")
    if not config.PINECONE_API_KEY:
        missing_vars.append("PINECONE_API_KEY")
    if not config.PINECONE_ENVIRONMENT:
        missing_vars.append("PINECONE_ENVIRONMENT")
    
    if missing_vars:
        error_msg = f"Missing required environment variables: {', '.join(missing_vars)}\n"
        error_msg += "Please ensure these variables are set in your .env file or environment."
        raise ValueError(error_msg)

# Update the initialize_components function
@st.cache_resource
def initialize_components():
    try:
        # Check environment variables first
        check_environment()
        pc = Pinecone(
            api_key=config.PINECONE_API_KEY,
            environment=config.PINECONE_ENVIRONMENT
        )
        
        # return {
        #     'embedding_manager': EmbeddingManager(),
        #     'vector_store': VectorStore(),
        #     'llm_manager': LLMManager()
        # }
        components = {
            'embedding_manager': EmbeddingManager(),
            'vector_store': VectorStore(),
            'llm_manager': LLMManager()
        }
        
        # Verify Pinecone index exists and is accessible
        index = pc.Index(config.PINECONE_INDEX_NAME)
        index_stats = index.describe_index_stats()
        st.sidebar.write(f"Pinecone Index Stats: {index_stats.total_vector_count} vectors")
        
        return components
    except Exception as e:
        st.error(f"Initialization Error: {str(e)}")
        st.info("Please check your .env file and ensure all required API keys are set correctly.")
        return None
    

components = initialize_components()

if components is None:
    st.stop()

embedding_manager = components['embedding_manager']
vector_store = components['vector_store']
llm_manager = components['llm_manager']

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "current_sources" not in st.session_state:
    st.session_state.current_sources = []
if "context_window" not in st.session_state:
    st.session_state.context_window = 5
if "max_history" not in st.session_state:
    st.session_state.max_history = 10

st.title(config.APP_TITLE)

# Chat interface
user_input = render_chat_interface(
    st.session_state.chat_history,
    st.session_state.current_sources
)

################### new


# Update the query processing in the main chat interface
if user_input:
    # Add user message to chat history
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_input
    })
    
    # Create a placeholder for the streaming response
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        
        try:
            # Generate embedding for query
            st.write("Debug: Generating query embedding...")
            query_embedding = embedding_manager.generate_embeddings([user_input])[0]
            st.write(f"Debug: Embedding generated, shape: {len(query_embedding)}")
            
            # Search for relevant documents
            st.write("Debug: Searching for relevant documents...")
            relevant_docs = vector_store.search(
                user_input,
                query_embedding,
                k=st.session_state.context_window
            )
            st.write(f"Debug: Found {len(relevant_docs)} relevant documents")
            
            # Generate streaming response
            st.write("Debug: Generating LLM response...")
            response = llm_manager.generate_response(
                user_input,
                relevant_docs,
                st.session_state.chat_history[-st.session_state.max_history:],
                streaming_container=response_placeholder
            )
            
            # Update chat history and sources
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": response
            })
            st.session_state.current_sources = relevant_docs
            
        except Exception as e:
            st.error(f"An error occurred during query processing: {str(e)}")
            st.error("Full error details:", exc_info=True)
    
    # Rerun to update UI
    st.rerun()

# Add a debug section in the sidebar
with st.sidebar:
    st.write("### Debug Information")
    if st.checkbox("Show Debug Info"):
        st.write("Pinecone Index:", config.PINECONE_INDEX_NAME)
        try:
            index = Pinecone.Index(config.PINECONE_INDEX_NAME)
            stats = index.describe_index_stats()
            st.write("Index Statistics:", stats)
        except Exception as e:
            st.error(f"Error fetching index stats: {str(e)}")


########## working ###########

# if user_input:
#     # Add user message to chat history
#     st.session_state.chat_history.append({
#         "role": "user",
#         "content": user_input
#     })
    
#     # Create a placeholder for the streaming response
#     with st.chat_message("assistant"):
#         response_placeholder = st.empty()
        
#         try:
#             # Generate embedding for query
#             query_embedding = embedding_manager.generate_embeddings([user_input])[0]
            
#             # Search for relevant documents
#             relevant_docs = vector_store.search(
#                 user_input,
#                 query_embedding,
#                 k=st.session_state.context_window
#             )
            
#             # Generate streaming response
#             response = llm_manager.generate_response(
#                 user_input,
#                 relevant_docs,
#                 st.session_state.chat_history[-st.session_state.max_history:],
#                 streaming_container=response_placeholder
#             )
            
#             # Update chat history and sources
#             st.session_state.chat_history.append({
#                 "role": "assistant",
#                 "content": response
#             })
#             st.session_state.current_sources = relevant_docs
            
#         except Exception as e:
#             st.error(f"An error occurred: {str(e)}")
    
#     # Rerun to update UI
#     st.rerun()



