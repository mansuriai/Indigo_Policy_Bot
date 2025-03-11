# core/index_website_content.py
import os
import sys
import logging
from pathlib import Path

# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.web_scraper import IndigoWebScraper
from core.embeddings import EmbeddingManager
from core.vector_store import VectorStore
from utils.config import config

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main function to scrape and index website content."""
    logger.info("Starting website content indexing")
    
    # Initialize components
    scraper = IndigoWebScraper()
    embedding_manager = EmbeddingManager()
    vector_store = VectorStore()
    
    # Scrape all target sections
    logger.info("Scraping website content...")
    all_chunks = scraper.scrape_all_sections()
    
    if not all_chunks:
        logger.error("No content was scraped from the website")
        return
    
    logger.info(f"Successfully scraped {len(all_chunks)} chunks of content")
    
    # Generate embeddings
    logger.info("Generating embeddings...")
    embeddings = embedding_manager.generate_embeddings(
        [chunk['text'] for chunk in all_chunks]
    )
    
    # Upload to vector database
    logger.info("Uploading to vector database...")
    vector_store.add_documents(all_chunks, embeddings)
    
    logger.info("Website content indexing completed successfully")

if __name__ == "__main__":
    main()