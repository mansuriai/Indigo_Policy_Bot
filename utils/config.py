# # utils/config.py
# import os
# from transformers import AutoModel
# import ssl
# from pathlib import Path
# from dotenv import load_dotenv

# load_dotenv()

# class Config:
#     # Project structure
#     BASE_DIR = Path(__file__).parent.parent
#     DATA_DIR = BASE_DIR / "data"
#     DB_DIR = BASE_DIR / "storage" / "vectordb"

    
#     PDF_STORAGE_DIR = BASE_DIR / "storage" / "pdfs"
#     PDF_STORAGE_DIR.mkdir(parents=True, exist_ok=True)
    
#     # PDF viewer route
#     PDF_VIEWER_ROUTE = "/view-pdf"
    
#     # Create directories if they don't exist
#     DATA_DIR.mkdir(parents=True, exist_ok=True)
#     DB_DIR.mkdir(parents=True, exist_ok=True)
    
#     # Model settings
#     # Disable SSL verification (Not recommended for production)
#     # ssl._create_default_https_context = ssl._create_unverified_context

#     # EMBEDDING_MODEL = AutoModel.from_pretrained("sentence-transformers/all-mpnet-base-v2")
#     EMBEDDING_MODEL = "sentence-transformers/all-mpnet-base-v2"
#     LLM_MODEL = "gpt-3.5-turbo-0125"
    
#     # Document processing
#     CHUNK_SIZE = 1000
#     CHUNK_OVERLAP = 200
    
#     # API Keys
#     # OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
#     OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
#     # PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
#     PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
#     # PINECONE_API_KEY='pcsk_4GP1q8_AkfsfNVvkMpTE2CP2LnpXinyRvUUwFNdTLC8PbmCZtKANaRAajc6eMRp3rMZWSj'
#     PINECONE_ENVIRONMENT='us-east-1'
#     # Pinecone settings
#     # PINECONE_INDEX_NAME = "document-embeddings"
#     PINECONE_INDEX_NAME = "indigo-assistant"

#     if not OPENAI_API_KEY:
#         raise ValueError("OPENAI_API_KEY not found in environment variables")
#     if not PINECONE_API_KEY:
#         raise ValueError("PINECONE_API_KEY not found in environment variables")
#     if not PINECONE_ENVIRONMENT:
#         raise ValueError("PINECONE_ENVIRONMENT not found in environment variables")
    
#     # App settings
#     APP_TITLE = "IndiGo Policies Chatbot"
#     MAX_HISTORY_LENGTH = 10
    
#     # Vector DB settings
#     COLLECTION_NAME = "indigo-documents"
#     DISTANCE_METRIC = "cosine"
    
#     ########### Temporary local storage
#     TEMP_DIR = BASE_DIR / "temp"
#     TEMP_DIR.mkdir(parents=True, exist_ok=True)


#     ############
#     RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"
#     RERANKER_BATCH_SIZE = 32
#     MIN_RELEVANCE_SCORE = 0.3
    
#     # Performance settings
#     EMBEDDING_BATCH_SIZE = 32
#     USE_GPU = False  # Set to True if GPU is available
#     CACHE_DIR = BASE_DIR / "storage" / "cache"
    
#     # Create cache directory
#     CACHE_DIR.mkdir(parents=True, exist_ok=True)

    
# config = Config()







######################

# utils/config.py
import os
#
# os.environ['CURL_CA_BUNDLE'] = ''
# os.environ['REQUESTS_CA_BUNDLE'] = ''
from pathlib import Path
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
load_dotenv()

class Config:
    # Project structure
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / "data"
    DB_DIR = BASE_DIR / "storage" / "vectordb"
    # MODEL_DIR = BASE_DIR / "models" / "all-mpnet-base-v2"   ####
    
    # Create directories if they don't exist
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    DB_DIR.mkdir(parents=True, exist_ok=True)
    
    # Model settings
    EMBEDDING_MODEL = SentenceTransformer("all-mpnet-base-v2")
    EMBEDDING_MODEL = "sentence-transformers/all-mpnet-base-v2" #"multi-qa-mpnet-base-dot-v1"# "sentence-transformers/all-mpnet-base-v2"   
    # EMBEDDING_MODEL = str(MODEL_DIR)
    LLM_MODEL = "gpt-4o-mini"
    
    # Document processing
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200

    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # Pinecone settings
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT", "gcp-starter")
    PINECONE_INDEX_NAME = "indigo-assistant" #os.getenv("PINECONE_INDEX_NAME", "indigo-assistant")
    
    # App settings
    APP_TITLE = "GoAssist"
    MAX_HISTORY_LENGTH = 5
    
    # Vector DB settings
    COLLECTION_NAME = "indigo-documents"
    DISTANCE_METRIC = "cosine"

    EMBEDDING_DIMENSION = 768  # Adjust based on your specific embedding model
    
    # Pinecone index settings
    PINECONE_INDEX_SPEC = {
        "cloud": "aws",
        "region": "us-east-1",
        "metric": "cosine"
    }
    
    # Web scraping settings
    WEB_SCRAPING_DELAY = 1  # Delay between requests in seconds
    
config = Config()