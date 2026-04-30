import logging
from typing import List, Dict, Any
from duckduckgo_search import DDGS
from backend.providers.base import SearchProvider
from backend.utils.retry import retry_with_backoff

logger = logging.getLogger(__name__)

class DuckDuckGoProvider(SearchProvider):
    def search_linkedin(self, query: str, max_results: int = 50) -> List[Dict[str, Any]]:
        """
        Uses DuckDuckGo to search for LinkedIn profiles.
        Query format: site:linkedin.com/in <query>
        Used as fallback when SerpAPI is unavailable.
        Note: DDG has unreliable site: operator support for LinkedIn — expect fewer results.
        """
        full_query = f'site:linkedin.com/in {query}'
        logger.info(f"[DDG Fallback] Executing search: {full_query}")

        def _do_search():
            results = []
            with DDGS() as ddgs:
                for r in ddgs.text(full_query, max_results=max_results):
                    results.append(r)
            return results

        try:
            results = retry_with_backoff(_do_search, retries=2, initial_delay=1.0)
            logger.info(f"[DDG Fallback] Returned {len(results)} raw results.")
            return results if results is not None else []
        except Exception as e:
            logger.error(f"[DDG Fallback] Search failed after retries: {e}")
            return []