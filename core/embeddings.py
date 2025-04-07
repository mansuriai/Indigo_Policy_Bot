# core/embeddings.py
from langchain_community.embeddings import HuggingFaceEmbeddings
import os
# from snowflake_arctic_embed import ArcticEmbeddings
from utils.config import config
from typing import List

class EmbeddingManager:
    def __init__(self): 
        print(f"Loading model from: {config.EMBEDDING_MODEL}")
        # Verify environment variable is set
        assert 'HF_ENDPOINT' in os.environ, "HF_ENDPOINT not set!"
        # Make sure we're using the correct model with the right dimensions
        self.model = HuggingFaceEmbeddings(
            model_name=config.EMBEDDING_MODEL,
            # model_name=config.EMBEDDING_MODEL,
            model_kwargs={'device': 'cpu', "trust_remote_code": True },
            encode_kwargs={'normalize_embeddings': True},
        )
        # self.model = ArcticEmbeddings(model_name="Snowflake/snowflake-arctic-embed-l-v2.0")
        # Add a dimension check during initialization
        test_embedding = self.model.embed_documents(["Test dimension check"])
        if test_embedding and len(test_embedding[0]) != config.EMBEDDING_DIMENSION:
            raise ValueError(f"Model produces embeddings with dimension {len(test_embedding[0])}, but config.EMBEDDING_DIMENSION is set to {config.EMBEDDING_DIMENSION}")
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of texts."""
        embeddings = self.model.embed_documents(texts)
        
        # Double-check dimensions before returning
        if embeddings and len(embeddings[0]) != config.EMBEDDING_DIMENSION:
            raise ValueError(f"Generated embeddings have dimension {len(embeddings[0])}, but expected {config.EMBEDDING_DIMENSION}")
            
        return embeddings