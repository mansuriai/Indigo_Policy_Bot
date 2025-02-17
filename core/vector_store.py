# core/vector_store.py
from typing import List, Dict, Optional
import chromadb
from chromadb.config import Settings
import numpy as np
from utils.config import config
from utils.s3_manager import S3Manager


class VectorStore:
    def __init__(self):
        self.s3_manager = S3Manager()
        self.client = chromadb.PersistentClient(
            path=str(config.TEMP_DIR / "vectordb"),
            settings=Settings(
                anonymized_telemetry=False,
                is_persistent=True,
                allow_reset=True
            )
        )
        self.collection = self._get_or_create_collection()
        self._initialize_cache()
        self._load_from_s3()
        ## working ##
        # self.client = chromadb.PersistentClient(
        #     path=str(config.DB_DIR),
        #     settings=Settings(
        #         anonymized_telemetry=False,
        #         is_persistent=True,
        #         allow_reset=True
        #     )
        # )
        # self.collection = self._get_or_create_collection()
        # self._initialize_cache()
    
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
    
    def add_documents(self, documents: List[Dict[str, str]], embeddings: List[List[float]]):
        """Add documents and their embeddings to the vector store."""
        # Batch processing for better performance
        batch_size = 100
        for i in range(0, len(documents), batch_size):
            batch_docs = documents[i:i + batch_size]
            batch_embeddings = embeddings[i:i + batch_size]
            
            self.collection.add(
                documents=[doc['text'] for doc in batch_docs],
                embeddings=batch_embeddings,
                metadatas=[doc['metadata'] for doc in batch_docs],
                ids=[doc['metadata']['chunk_id'] for doc in batch_docs]
            )
    
    def search(self, query: str, embedding: List[float], k: int = 3) -> List[Dict]:
        """Search for similar documents with caching."""
        cache_key = self._get_cache_key(query)
        
        # Check cache first
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=k,
            include=["documents", "metadatas", "distances"]
        )
        
        processed_results = [{
            'text': doc,
            'metadata': meta,
            'distance': dist
        } for doc, meta, dist in zip(
            results['documents'][0],
            results['metadatas'][0],
            results['distances'][0]
        )]
        
        # Update cache
        if len(self.cache) >= self.cache_size:
            # Remove oldest entry
            self.cache.pop(next(iter(self.cache)))
        self.cache[cache_key] = processed_results
        
        return processed_results
    

    #####################################
    def _load_from_s3(self):
        """Load vector store data from S3."""
        try:
            db_path = config.TEMP_DIR / "vectordb"
            if not db_path.exists():
                # Download vectordb from S3
                s3_files = self.s3_manager.list_files(config.S3_VECTORDB_PREFIX)
                for s3_key in s3_files:
                    local_path = config.TEMP_DIR / "vectordb" / Path(s3_key).name
                    local_path.parent.mkdir(parents=True, exist_ok=True)
                    self.s3_manager.download_file(s3_key, local_path)
        except Exception as e:
            print(f"Error loading vector store from S3: {e}")
    
    def _save_to_s3(self):
        """Save vector store data to S3."""
        try:
            db_path = config.TEMP_DIR / "vectordb"
            for file_path in db_path.rglob("*"):
                if file_path.is_file():
                    relative_path = file_path.relative_to(db_path)
                    s3_key = f"{config.S3_VECTORDB_PREFIX}{relative_path}"
                    self.s3_manager.upload_file(file_path, s3_key)
        except Exception as e:
            print(f"Error saving vector store to S3: {e}")
    
    def add_documents(self, documents: List[Dict[str, str]], embeddings: List[List[float]]):
        """Add documents and their embeddings to the vector store."""
        super().add_documents(documents, embeddings)
        self._save_to_s3()

