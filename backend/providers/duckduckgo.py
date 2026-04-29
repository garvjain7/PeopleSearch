import logging
from typing import List, Dict, Any
from duckduckgo_search import DDGS
from .base import SearchProvider
from backend.utils.retry import retry_with_backoff

logger = logging.getLogger(__name__)

class DuckDuckGoProvider(SearchProvider):
    def search_linkedin(self, query: str, max_results: int = 50) -> List[Dict[str, Any]]:
        """
        Uses DuckDuckGo to search for LinkedIn profiles.
        Query format: site:linkedin.com/in <query>
        """
        full_query = f'site:linkedin.com/in {query}'
        logger.info(f"Executing DDG search: {full_query}")
        
        def _do_search():
            results = []
            with DDGS() as ddgs:
                # ddgs.text returns an iterator. We fetch up to max_results.
                ddg_results = ddgs.text(full_query, max_results=max_results)
                for r in ddg_results:
                    results.append(r)
            return results

        try:
            # We use retry_with_backoff to handle potential rate limiting
            return retry_with_backoff(_do_search, retries=3, initial_delay=2.0)
        except Exception as e:
            logger.error(f"DuckDuckGo search failed: {e}")
            return []
