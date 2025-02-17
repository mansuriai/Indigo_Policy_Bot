# # app/components/sidebar.py
# import streamlit as st
# from pathlib import Path
# from utils.config import config

# def render_sidebar():
#     """Render the sidebar with file upload and settings."""
#     with st.sidebar:
#         st.header("Document Upload")
        
#         uploaded_files = st.file_uploader(
#             "Upload PDF documents",
#             type=['pdf'],
#             accept_multiple_files=True
#         )
        
#         if uploaded_files:
#             for file in uploaded_files:
#                 file_path = config.DATA_DIR / file.name
#                 with open(file_path, 'wb') as f:
#                     f.write(file.getvalue())
            
#             st.success(f"Uploaded {len(uploaded_files)} documents")
            
#         st.divider()
        
#         with st.expander("Settings"):
#             st.slider(
#                 "Context window",
#                 min_value=1,
#                 max_value=5,
#                 value=3,
#                 key="context_window"
#             )
            
#             st.slider(
#                 "Chat history length",
#                 min_value=1,
#                 max_value=10,
#                 value=config.MAX_HISTORY_LENGTH,
#                 key="max_history"
#             )
        
#         return uploaded_files