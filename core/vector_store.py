# core/vector_store.py
from pinecone import Pinecone, ServerlessSpec
from typing import List, Dict, Optional
import chromadb
from chromadb.config import Settings
import numpy as np
import streamlit as st
from utils.config import config
# from utils.s3_manager import S3Manager
import urllib3
import ssl
import requests
import traceback
import logging

#################
## Please comment this line while working on local machine
# import sys
# sys.modules["sqlite3"] = __import__("pysqlite3")
####################
# Disable SSL verification for urllib3
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class VectorStore:
    # def __init__(self):

    #     # Create a custom SSL context that doesn't verify certificates
    #     # ssl_context = ssl.create_default_context()
    #     # ssl_context.check_hostname = False
    #     # ssl_context.verify_mode = ssl.CERT_NONE
        
    #     # # Set up a custom HTTP pool with our SSL context
    #     # http = urllib3.PoolManager(
    #     #     ssl_context=ssl_context,
    #     #     cert_reqs='CERT_NONE'
    #     # )

    #     session = requests.Session()
    #     session.verify = False

    #     pc = Pinecone(
    #         api_key=config.PINECONE_API_KEY,
    #         environment=config.PINECONE_ENVIRONMENT
    #     )

    #     # Monkey patch the Pinecone client's HTTP pool if needed
    #     # try:
    #     #     for client in [pc.control_client, pc.data_client]:
    #     #         if hasattr(client, 'pool_manager'):
    #     #             client.pool_manager = http
    #     # except:
    #     #     pass  # Skip if this structure has changed

    #     print(f"Connecting to Pinecone with API key: {config.PINECONE_API_KEY[:5]}... and environment: {config.PINECONE_ENVIRONMENT}")

    #     # if config.PINECONE_INDEX_NAME not in pc.list_indexes().names():
    #     #     pc.create_index(
    #     #         name=config.PINECONE_INDEX_NAME,
    #     #         dimension=768,
    #     #         metric='cosine',
    #     #         spec=ServerlessSpec(
    #     #             cloud='aws',
    #     #             region='us-east-1'
    #     #         )
    #     #     )

    #     # Check if index exists with SSL workaround
    #     try:
    #         # Attempt to create the index if it doesn't exist
    #         try:
    #             index_list = pc.list_indexes().names()
    #             if config.PINECONE_INDEX_NAME not in index_list:
    #                 print(f"Creating index: {config.PINECONE_INDEX_NAME}")
    #                 pc.create_index(
    #                     name=config.PINECONE_INDEX_NAME,
    #                     dimension=768,
    #                     metric='cosine',
    #                     spec=ServerlessSpec(
    #                         cloud='aws',
    #                         region='us-east-1'
    #                     )
    #                 )
    #         except Exception as e:
    #             print(f"Could not check or create index: {e}")
    #             print("Assuming index already exists and continuing...")
            
    #         # Connect to the index
    #         self.index = pc.Index(config.PINECONE_INDEX_NAME)
    #         self._initialize_cache()
    #     except Exception as e:
    #         print(f"Error initializing Pinecone: {e}")
    #         # Create a fallback option
    #         st.error(f"Could not connect to Pinecone: {e}")
    #         raise
    #         # Attempt to proceed anyway assuming index exists
        
    #     # self.index = pc.Index(config.PINECONE_INDEX_NAME)
    #     # self._initialize_cache()

    def __init__(self):
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        try:
            # Initialize Pinecone with retries and detailed logging
            self.pc = Pinecone(
                api_key=config.PINECONE_API_KEY,
                environment=config.PINECONE_ENVIRONMENT
            )

            # Verify index exists or create it
            self._ensure_index_exists()

            # Connect to the index
            self.index = self.pc.Index(config.PINECONE_INDEX_NAME)
            
            # Log successful initialization
            self.logger.info(f"Successfully connected to Pinecone index: {config.PINECONE_INDEX_NAME}")

        except Exception as e:
            # Detailed error logging
            self.logger.error(f"Pinecone Initialization Error: {str(e)}")
            self.logger.error(traceback.format_exc())
            raise

    def _ensure_index_exists(self):
        """Ensure the Pinecone index exists, create if necessary."""
        try:
            # List existing indexes
            existing_indexes = self.pc.list_indexes().names()
            
            # Create index if it doesn't exist
            if config.PINECONE_INDEX_NAME not in existing_indexes:
                self.logger.info(f"Creating Pinecone index: {config.PINECONE_INDEX_NAME}")
                self.pc.create_index(
                    name=config.PINECONE_INDEX_NAME,
                    dimension=768,  # Ensure this matches your embedding dimension
                    metric='cosine',
                    spec=ServerlessSpec(
                        cloud='aws',
                        region='us-east-1'
                    )
                )
                self.logger.info(f"Index {config.PINECONE_INDEX_NAME} created successfully")
        
        except Exception as e:
            self.logger.error(f"Error ensuring index exists: {str(e)}")
            raise
    
    def _initialize_cache(self):
        """Initialize an in-memory cache for frequent queries."""
        self.cache = {}
        self.cache_size = 1000  # This can be Adjusted based on our needs
    
    def _get_cache_key(self, query: str) -> str:
        """Generate a cache key for a query."""
        return str(hash(query))
    
    def _get_or_create_collection(self):
        """Get existing collection or create new one."""
        try:
            return self.client.get_collection(config.COLLECTION_NAME)
        except:
            return self.client.create_collection(
                name=config.COLLECTION_NAME,
                metadata={"hnsw:space": config.DISTANCE_METRIC}
            )
    

    ########################### new pinecone #####################

    # def add_documents(self, documents: List[Dict[str, str]], embeddings: List[List[float]]):
    #     """Add documents and their embeddings to Pinecone."""
    #     batch_size = 100
    #     for i in range(0, len(documents), batch_size):
    #         batch_docs = documents[i:i + batch_size]
    #         batch_embeddings = embeddings[i:i + batch_size]
            
    #         vectors = []
    #         for doc, embedding in zip(batch_docs, batch_embeddings):
    #             vectors.append({
    #                 'id': doc['metadata']['chunk_id'],
    #                 'values': embedding,
    #                 'metadata': {
    #                     'text': doc['text'],
    #                     **doc['metadata']
    #                 }
    #             })
            
    #         # self.index.upsert(vectors=vectors)
    #         try:
    #             self.index.upsert(vectors=vectors)
    #             print(f"Successfully upserted {len(vectors)} vectors")
    #         except Exception as e:
    #             print(f"Error upserting vectors: {e}")

    # def search(self, query: str, embedding: List[float], k: int = 3) -> List[Dict]:
    #     """Search for similar documents in Pinecone with logging."""
    #     try:
    #         # st.write("Debug: Searching Pinecone index...")
    #         # st.write(f"Debug: Query length: {len(embedding)} dimensions")
            
    #         # Query Pinecone
    #         results = self.index.query(
    #             vector=embedding,
    #             top_k=k,
    #             include_metadata=True
    #         )
            
    #         st.write(f"Debug: Found {len(results.matches)} matches")
            
    #         processed_results = []
    #         for match in results.matches:
    #             processed_results.append({
    #                 'text': match.metadata['text'],
    #                 'metadata': {k: v for k, v in match.metadata.items() if k != 'text'},
    #                 'distance': 1 - match.score  # Convert cosine similarity to distance
    #             })
            
    #         return processed_results
            
    #     except Exception as e:
    #         st.error(f"Error during vector search: {str(e)}")
    #         raise
    def add_documents(self, documents: List[Dict[str, str]], embeddings: List[List[float]]):
        """Add documents and their embeddings to Pinecone with improved error handling."""
        try:
            batch_size = 100
            for i in range(0, len(documents), batch_size):
                batch_docs = documents[i:i + batch_size]
                batch_embeddings = embeddings[i:i + batch_size]
                
                vectors = []
                for doc, embedding in zip(batch_docs, batch_embeddings):
                    vectors.append({
                        'id': doc['metadata'].get('chunk_id', str(hash(doc['text']))),
                        'values': embedding,
                        'metadata': {
                            'text': doc['text'],
                            **doc.get('metadata', {})
                        }
                    })
                
                try:
                    self.index.upsert(vectors=vectors)
                    self.logger.info(f"Successfully upserted {len(vectors)} vectors")
                except Exception as batch_error:
                    self.logger.error(f"Error upserting batch: {str(batch_error)}")
        
        except Exception as e:
            self.logger.error(f"Document addition error: {str(e)}")
            raise

    def search(self, query: str, embedding: List[float], k: int = 3) -> List[Dict]:
        """Search for similar documents in Pinecone with comprehensive error handling."""
        try:
            # Validate embedding
            if not embedding or len(embedding) == 0:
                raise ValueError("Invalid embedding: Empty or None")
            
            # Query Pinecone
            results = self.index.query(
                vector=embedding,
                top_k=k,
                include_metadata=True
            )
            
            processed_results = []
            for match in results.matches:
                processed_results.append({
                    'text': match.metadata.get('text', ''),
                    'metadata': {k: v for k, v in match.metadata.items() if k != 'text'},
                    'distance': 1 - match.score  # Convert cosine similarity to distance
                })
            
            return processed_results
            
        except Exception as e:
            self.logger.error(f"Vector search error: {str(e)}")
            self.logger.error(traceback.format_exc())
            raise