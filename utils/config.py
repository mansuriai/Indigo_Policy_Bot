# utils/config.py
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Project structure
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / "data"
    DB_DIR = BASE_DIR / "storage" / "vectordb"
    
    # Create directories if they don't exist
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    DB_DIR.mkdir(parents=True, exist_ok=True)
    
    # Model settings
    EMBEDDING_MODEL = "sentence-transformers/all-mpnet-base-v2"
    LLM_MODEL = "gpt-3.5-turbo-0125"
    
    # Document processing
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    
    # API Keys
    # OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    # PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    # PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
    PINECONE_API_KEY='pcsk_4GP1q8_AkfsfNVvkMpTE2CP2LnpXinyRvUUwFNdTLC8PbmCZtKANaRAajc6eMRp3rMZWSj'
    PINECONE_ENVIRONMENT='us-east-1'
    # Pinecone settings
    PINECONE_INDEX_NAME = "document-embeddings"

    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    if not PINECONE_API_KEY:
        raise ValueError("PINECONE_API_KEY not found in environment variables")
    if not PINECONE_ENVIRONMENT:
        raise ValueError("PINECONE_ENVIRONMENT not found in environment variables")
    
    # App settings
    APP_TITLE = "IndiGo Policies Chatbot"
    MAX_HISTORY_LENGTH = 10
    
    # Vector DB settings
    COLLECTION_NAME = "documents"
    DISTANCE_METRIC = "cosine"
    
    ########### Temporary local storage
    TEMP_DIR = BASE_DIR / "temp"
    TEMP_DIR.mkdir(parents=True, exist_ok=True)


    ############
    RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"
    RERANKER_BATCH_SIZE = 32
    MIN_RELEVANCE_SCORE = 0.3
    
    # Performance settings
    EMBEDDING_BATCH_SIZE = 32
    USE_GPU = False  # Set to True if GPU is available
    CACHE_DIR = BASE_DIR / "storage" / "cache"
    
    # Create cache directory
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    
config = Config()