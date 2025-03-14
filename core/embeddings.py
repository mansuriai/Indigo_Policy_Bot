# core/embeddings.py
from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain_huggingface import HuggingFaceEmbeddings
import os
from utils.config import config
from typing import List

class EmbeddingManager:
    # def __init__(self):
        # print(config.EMBEDDING_MODEL)
        # self.model = HuggingFaceEmbeddings(
        #     model_name=config.EMBEDDING_MODEL,
        #     model_kwargs={'device': 'cpu'},
        #     encode_kwargs={'normalize_embeddings': True}
        # )

    def __init__(self):
        # os.environ['CURL_CA_BUNDLE'] = ''
        # os.environ['REQUESTS_CA_BUNDLE'] = ''
        # os.environ['HF_HUB_DISABLE_SSL_VERIFICATION'] = '1'

        print(f"Loading model from: {config.EMBEDDING_MODEL}")
        self.model = HuggingFaceEmbeddings(
            model_name=config.EMBEDDING_MODEL,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True},
            # request_kwargs={"verify": False}  # Add this line to disable SSL verification
        )
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of texts."""
        return self.model.embed_documents(texts)