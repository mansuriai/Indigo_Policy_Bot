# app/upload_app.py
import streamlit as st
from pathlib import Path
import time
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.config import config
from utils.s3_manager import S3Manager
from core.document_processor import EnhancedDocumentProcessor
from core.embeddings import EmbeddingManager
from core.vector_store import VectorStore

# Initialize session state
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []

# Initialize components
doc_processor = EnhancedDocumentProcessor()
embedding_manager = EmbeddingManager()
vector_store = VectorStore()

st.set_page_config(
    page_title=f"{config.APP_TITLE} - Document Upload",
    layout="wide"
)

st.title(f"{config.APP_TITLE} - Document Upload")

############################   S3####################
# def process_and_upload_file(file, doc_processor, embedding_manager, vector_store, s3_manager):
#     """Process a file and upload to S3."""
#     # Save file temporarily
#     temp_file_path = config.TEMP_DIR / file.name
#     with open(temp_file_path, 'wb') as f:
#         f.write(file.getvalue())
    
#     try:
#         # Upload original file to S3
#         s3_key = f"{config.S3_DOCUMENTS_PREFIX}{file.name}"
#         s3_manager.upload_file(temp_file_path, s3_key)
        
#         # Process document
#         chunks = doc_processor.process_file(temp_file_path)
        
#         # Generate embeddings
#         embeddings = embedding_manager.generate_embeddings(
#             [chunk['text'] for chunk in chunks]
#         )
        
#         # Store in vector database (which will handle S3 sync)
#         vector_store.add_documents(chunks, embeddings)
        
#         return True
#     except Exception as e:
#         st.error(f"Error processing {file.name}: {str(e)}")
#         return False
#     finally:
#         # Clean up temporary file
#         temp_file_path.unlink(missing_ok=True)

###########################


# File upload section
st.header("Upload Documents")
uploaded_files = st.file_uploader(
    "Upload PDF documents",
    type=['pdf'],
    accept_multiple_files=True
)

if uploaded_files:
    st.session_state.uploaded_files = uploaded_files

if st.session_state.uploaded_files:
    st.write(f"{len(st.session_state.uploaded_files)} documents ready for processing.")
    
    if st.button("Process Documents"):
        with st.spinner("Processing documents..."):
            for file in st.session_state.uploaded_files:
                file_path = config.DATA_DIR / file.name
                with open(file_path, 'wb') as f:
                    f.write(file.getvalue())
                
                # Process documents
                chunks = doc_processor.process_file(file_path)
                
                # Generate embeddings
                embeddings = embedding_manager.generate_embeddings(
                    [chunk['text'] for chunk in chunks]
                )
                
                # Store in vector database
                vector_store.add_documents(chunks, embeddings)
            
            st.success("Documents processed and indexed!")
            st.session_state.uploaded_files = []  # Clear uploaded files after processing




###############      S3 #######################
# Update main upload app
# def main():
#     st.set_page_config(
#         page_title=f"{config.APP_TITLE} - Document Upload",
#         layout="wide"
#     )
    
#     st.title(f"{config.APP_TITLE} - Document Upload")
    
#     # Initialize S3 manager
#     s3_manager = S3Manager()
    
#     # File upload section
#     uploaded_files = st.file_uploader(
#         "Upload PDF documents",
#         type=['pdf'],
#         accept_multiple_files=True
#     )
    
#     if uploaded_files:
#         st.write(f"{len(uploaded_files)} documents ready for processing.")
        
#         if st.button("Process Documents"):
#             progress_bar = st.progress(0)
#             for i, file in enumerate(uploaded_files):
#                 with st.spinner(f"Processing {file.name}..."):
#                     success = process_and_upload_file(
#                         file,
#                         doc_processor,
#                         embedding_manager,
#                         vector_store,
#                         s3_manager
#                     )
#                     if success:
#                         st.success(f"Successfully processed {file.name}")
#                     progress_bar.progress((i + 1) / len(uploaded_files))
            
#             st.success("All documents processed and uploaded!")

# if __name__ == "__main__":
#     main()
##########################################