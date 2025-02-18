# core/vector_store.py
from pinecone import Pinecone, ServerlessSpec
from typing import List, Dict, Optional
import chromadb
from chromadb.config import Settings
import numpy as np
import streamlit as st
from utils.config import config
# from utils.s3_manager import S3Manager

#################
## Please comment this line while working on local machine
import sys
sys.modules["sqlite3"] = __import__("pysqlite3")
####################


class VectorStore:
    def __init__(self):

        pc = Pinecone(
            api_key=config.PINECONE_API_KEY,
            environment=config.PINECONE_ENVIRONMENT
        )

        print(f"{config.PINECONE_API_KEY} and {config.PINECONE_ENVIRONMENT} and {config.PINECONE_INDEX_NAME}")

        if config.PINECONE_INDEX_NAME not in pc.list_indexes().names():
            pc.create_index(
                name=config.PINECONE_INDEX_NAME,
                dimension=768,
                metric='cosine',
                spec=ServerlessSpec(
                    cloud='aws',
                    region='us-east-1'
                )
            )
        
        self.index = pc.Index(config.PINECONE_INDEX_NAME)
        self._initialize_cache()
    
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

    def add_documents(self, documents: List[Dict[str, str]], embeddings: List[List[float]]):
        """Add documents and their embeddings to Pinecone."""
        batch_size = 100
        for i in range(0, len(documents), batch_size):
            batch_docs = documents[i:i + batch_size]
            batch_embeddings = embeddings[i:i + batch_size]
            
            vectors = []
            for doc, embedding in zip(batch_docs, batch_embeddings):
                vectors.append({
                    'id': doc['metadata']['chunk_id'],
                    'values': embedding,
                    'metadata': {
                        'text': doc['text'],
                        **doc['metadata']
                    }
                })
            
            self.index.upsert(vectors=vectors)

    def search(self, query: str, embedding: List[float], k: int = 3) -> List[Dict]:
        """Search for similar documents in Pinecone with logging."""
        try:
            st.write("Debug: Searching Pinecone index...")
            st.write(f"Debug: Query length: {len(embedding)} dimensions")
            
            # Query Pinecone
            results = self.index.query(
                vector=embedding,
                top_k=k,
                include_metadata=True
            )
            
            st.write(f"Debug: Found {len(results.matches)} matches")
            
            processed_results = []
            for match in results.matches:
                processed_results.append({
                    'text': match.metadata['text'],
                    'metadata': {k: v for k, v in match.metadata.items() if k != 'text'},
                    'distance': 1 - match.score  # Convert cosine similarity to distance
                })
            
            return processed_results
            
        except Exception as e:
            st.error(f"Error during vector search: {str(e)}")
            raise