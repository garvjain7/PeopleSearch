import logging
import requests
from typing import List, Dict, Any
from .base import SearchProvider
from backend.config.settings import settings

logger = logging.getLogger(__name__)

class SerpAPIProvider(SearchProvider):
    def search_linkedin(self, query: str, max_results: int = 50) -> List[Dict[str, Any]]:
        """
        Uses SerpAPI (Google Search) as a reliable production fallback.
        Requires SERPAPI_KEY in environment/settings.
        """
        if not settings.SERPAPI_KEY:
            logger.warning("SerpAPI key is missing. Cannot execute fallback search.")
            return []
            
        logger.info(f"Executing SerpAPI search for: {query}")
        
        params = {
            "engine": "google",
            "q": f"site:linkedin.com/in {query}",
            "api_key": settings.SERPAPI_KEY,
            "num": max_results
        }
        
        try:
            response = requests.get("https://serpapi.com/search", params=params)
            response.raise_for_status()
            data = response.json()
            
            results = []
            for item in data.get("organic_results", []):
                # Map SerpAPI response to our standard format
                results.append({
                    "title": item.get("title", ""),
                    "body": item.get("snippet", ""),
                    "href": item.get("link", "")
                })
            return results
        except Exception as e:
            logger.error(f"SerpAPI search failed: {e}")
            return None
