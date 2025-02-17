# import streamlit as st
# from typing import Dict
# import sys
# import os

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
# from utils.config import config

# def show_source_page(source: Dict):
#     """Display source content in detail."""
#     st.title("Source Details")
    
#     st.markdown(f"### {source['metadata']['source']}")
#     st.markdown(f"**Page:** {source['metadata']['page_num']}")
    
#     if source['metadata'].get('content_type') == 'table':
#         st.markdown("#### Table Information")
#         st.markdown(f"- Table Number: {source['metadata'].get('table_num')}")
#         st.markdown(f"- Rows: {source['metadata'].get('row_count')}")
#         st.markdown(f"- Columns: {source['metadata'].get('col_count')}")
    
#     st.markdown("### Content")
#     st.markdown(source['text'])
    
#     st.markdown("### Metadata")
#     st.json(source['metadata'])

# def main():
#     st.set_page_config(
#         page_title=f"{config.APP_TITLE} - Source Viewer",
#         layout="wide"
#     )
    
#     # Get source key from URL parameters
#     query_params = st.experimental_get_query_params()
#     source_key = query_params.get("source_key", [None])[0]
    
#     if source_key and f"source_data_{source_key}" in st.session_state:
#         source = st.session_state[f"source_data_{source_key}"]
#         show_source_page(source)
#     else:
#         st.error("Source not found.")

# if __name__ == "__main__":
#     main()