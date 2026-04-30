import logging
import requests
from typing import List, Dict, Any
from .base import SearchProvider
from backend.config.settings import settings

logger = logging.getLogger(__name__)

class SerpAPIProvider(SearchProvider):
    def search_linkedin(self, query: str, max_results: int = 50) -> List[Dict[str, Any]]:
        """
        Uses SerpAPI (Google Search) as the primary provider.
        Requires SERPAPI_KEY in environment/settings.
        """
        if not settings.SERPAPI_KEY:
            logger.warning("[SerpAPI] SERPAPI_KEY is missing. Cannot execute search.")
            return []

        logger.info(f"[SerpAPI Primary] Executing search for: {query}")

        params = {
            "engine": "google",
            "q": f"site:linkedin.com/in {query}",
            "api_key": settings.SERPAPI_KEY,
            "num": max_results
        }

        try:
            response = requests.get("https://serpapi.com/search", params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            results = []
            for item in data.get("organic_results", []):
                results.append({
                    "title": item.get("title", ""),
                    "body": item.get("snippet", ""),
                    "href": item.get("link", "")
                })

            logger.info(f"[SerpAPI Primary] Returned {len(results)} raw results.")
            return results
        except Exception as e:
            logger.error(f"[SerpAPI Primary] Search failed: {e}")
            return []