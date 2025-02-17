# app/main.py
import streamlit as st
from pathlib import Path
import time
from typing import List, Dict
import os, sys
from urllib.parse import urlencode


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.apikey import OPENAIAPI
os.environ["OPENAI_API_KEY"] = OPENAIAPI

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


# Initialize components with error handling
@st.cache_resource
def initialize_components():
    try:
        return {
            'embedding_manager': EmbeddingManager(),
            'vector_store': VectorStore(),
            'llm_manager': LLMManager()
        }
    except Exception as e:
        st.error(f"Error initializing components: {str(e)}")
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
            query_embedding = embedding_manager.generate_embeddings([user_input])[0]
            
            # Search for relevant documents
            relevant_docs = vector_store.search(
                user_input,
                query_embedding,
                k=st.session_state.context_window
            )
            
            # Generate streaming response
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
            st.error(f"An error occurred: {str(e)}")
    
    # Rerun to update UI
    st.rerun()



# if user_input:
#     # Add user message to chat history
#     st.session_state.chat_history.append({
#         "role": "user",
#         "content": user_input
#     })
    
#     # Create a placeholder for the streaming response
#     response_placeholder = st.empty()
    
#     try:
#         # Generate embedding for query
#         query_embedding = embedding_manager.generate_embeddings([user_input])[0]
        
#         # Search for relevant documents
#         relevant_docs = vector_store.search(
#             user_input,
#             query_embedding,
#             k=st.session_state.context_window
#         )
        
#         # Generate streaming response
#         response = llm_manager.generate_response(
#             user_input,
#             relevant_docs,
#             st.session_state.chat_history[-st.session_state.max_history:],
#             streaming_container=response_placeholder
#         )
        
#         # Update chat history and sources
#         st.session_state.chat_history.append({
#             "role": "assistant",
#             "content": response
#         })
#         st.session_state.current_sources = relevant_docs
        
#     except Exception as e:
#         st.error(f"An error occurred: {str(e)}")
    
#     # Rerun to update UI
#     st.rerun()





