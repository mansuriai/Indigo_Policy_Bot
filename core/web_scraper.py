# core/web_scraper.py
import requests
from bs4 import BeautifulSoup
import time
from typing import List, Dict, Any, Optional
import logging
from langchain.text_splitter import RecursiveCharacterTextSplitter
from urllib.parse import urljoin

from utils.config import config
from utils.helpers import generate_document_id

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IndigoWebScraper:
    """Scrapes content from the Indigo Airlines website for specific sections."""
    
    def __init__(self):
        self.base_url = "https://www.goindigo.in"
        self.session = requests.Session()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
        }
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP,
            length_function=len,
        )
        
        # Define target sections to scrape
        # self.target_sections = {
        #     "support": "/information/at-the-airport/airport-facilities.html",
        #     "offers": "/deals-and-offers/6e-holiday-packages.html",
        #     "terms_conditions": "/information/booking/terms-and-conditions.html",
        #     "conditions_of_carriage": "/information/booking/conditions-of-carriage.html",
        #     "travel_tips": "/information/travel-information/international-travel-tips.html",
        #     "web_check_in": "/information/travel-information/web-check-in.html"
        # }

        self.target_sections = {
            "offers": "https://www.goindigo.in/campaigns/indigo-offers.html",
            "6e_offers": "https://www.goindigo.in/add-on-services/6exclusive-fare.html?linkNav=6exclusive+fare%7C1%7CFlight+offers",
            "student_discount": "https://www.goindigo.in/add-on-services/student-discount.html?linkNav=Student+discount%7C2%7CFlight+offers",
            "armed_forces": "https://www.goindigo.in/add-on-services/armed-forces.html?linkNav=Armed+forces%7C3%7CFlight+offers",
            "ajio_luxe": "https://www.goindigo.in/campaigns/ajioluxe-offers.html",
            "excess_baggage": "https://www.goindigo.in/add-on-services/excess-baggage.html?linkNav=Excess+baggage%7C1%7CAddons",
            "partner_offers": "https://www.goindigo.in/hotels.html?linkNav=6e-bagport%7C1%7CPartner+Offers",
            "senior_citizen": "https://www.goindigo.in/add-on-services/senior-citizen-discount.html?linkNav=Senior+Citizen%7C4%7CFlight+offers",
            "fast_forward": "https://www.goindigo.in/add-on-services/fast-forward.html?linkNav=Fast+forward%7C2%7CAddons",
            "terms_and_cond_offer": "https://www.goindigo.in/indigo-spotify/terms-and-conditions.html",
            "skyplus_6e": "https://www.goindigo.in/content/skyplus6e/in/en/mokobara.html?linkNav=6e-bagport%7C1%7CPartner+Offers",
            "terms_conditions": "https://www.goindigo.in/information/terms-and-conditions.html",
            "internation_travel_tips": "https://www.goindigo.in/information/useful-tips-for-your-international-flight.html",
            "web_checkin_advisory": "https://www.goindigo.in/web-check-in.html",
            "conditions_of_carriage": "https://www.goindigo.in/information/conditions-of-carriage.html",
            "faqs": "https://www.goindigo.in/travel-information/en.html",
            "indigo_cargo": "https://cargo.goindigo.in/",
            "contact_us": "https://www.goindigo.in/contact-us.html",
            "6e_skai": "https://www.goindigo.in/support.html",
            "hotels": "https://www.goindigo.in/hotels",
            "charters_services": "https://www.goindigo.in/charters.html",
            "refund_claim": "https://www.goindigo.in/initiate-refund.html",
            "baggage": "https://www.goindigo.in/baggage.html",
            "add_on_services": "https://www.goindigo.in/add-on-services.html",
            "6e_eat": "https://www.goindigo.in/add-on-services/food-menu.html",
            "seat_select": "https://www.goindigo.in/add-on-services/seat-plus.html",
            "special_disability_assistance": "https://www.goindigo.in/information/special-disability-assistance.html",
            "plan_b": "https://www.goindigo.in/plan-b.html"
        }
    
    def _get_page_content(self, url: str) -> Optional[str]:
        """Fetch content from a URL with error handling and rate limiting."""
        try:
            full_url = urljoin(self.base_url, url)
            logger.info(f"Fetching content from: {full_url}")
            
            # Rate limiting to be respectful to the website
            time.sleep(1)
            
            response = self.session.get(full_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            return response.text
        except requests.RequestException as e:
            logger.error(f"Error fetching {url}: {str(e)}")
            return None
    
    def _extract_content(self, html: str, section_name: str) -> Dict[str, Any]:
        """Extract relevant content from HTML based on section type."""
        soup = BeautifulSoup(html, 'html.parser')
        
        # Find the main content area - this may need adjustments based on website structure
        content_area = soup.select_one('.content-area, .page-content, article, .main-content')
        
        if not content_area:
            logger.warning(f"Could not find main content area for {section_name}")
            # Fallback to body
            content_area = soup.body
        
        # Extract the text content
        content_text = content_area.get_text(separator='\n', strip=True)
        
        # Create metadata
        metadata = {
            "source": f"indigo-website-{section_name}",
            "url": urljoin(self.base_url, self.target_sections[section_name]),
            "section": section_name,
            "scrape_timestamp": time.time()
        }
        
        return {"text": content_text, "metadata": metadata}
    
    def _process_content(self, content: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Split content into chunks and prepare for vectorization."""
        if not content or not content.get("text"):
            return []
        
        # Split text into manageable chunks
        chunks = self.text_splitter.split_text(content["text"])
        
        processed_chunks = []
        for i, chunk in enumerate(chunks):
            chunk_id = generate_document_id(f"{content['metadata']['section']}-{i}-{chunk}")
            
            processed_chunks.append({
                "text": chunk,
                "metadata": {
                    **content["metadata"],
                    "chunk_id": chunk_id,
                    "chunk_index": i,
                    "total_chunks": len(chunks)
                }
            })
        
        return processed_chunks
    
    def scrape_all_sections(self) -> List[Dict[str, Any]]:
        """Scrape all target sections and return processed chunks."""
        all_chunks = []
        
        for section_name, url_path in self.target_sections.items():
            html_content = self._get_page_content(url_path)
            
            if html_content:
                content = self._extract_content(html_content, section_name)
                chunks = self._process_content(content)
                all_chunks.extend(chunks)
                
                logger.info(f"Processed {len(chunks)} chunks from {section_name}")
            else:
                logger.warning(f"Failed to fetch content for {section_name}")
        
        return all_chunks
    
    def scrape_section(self, section_name: str) -> List[Dict[str, Any]]:
        """Scrape a specific section by name."""
        if section_name not in self.target_sections:
            logger.error(f"Unknown section: {section_name}")
            return []
        
        html_content = self._get_page_content(self.target_sections[section_name])
        
        if not html_content:
            return []
        
        content = self._extract_content(html_content, section_name)
        chunks = self._process_content(content)
        
        return chunks








