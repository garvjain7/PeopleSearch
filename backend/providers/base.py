from abc import ABC, abstractmethod
from typing import List, Dict, Any

class SearchProvider(ABC):
    @abstractmethod
    def search_linkedin(self, query: str, max_results: int = 50) -> List[Dict[str, Any]]:
        """
        Search LinkedIn via the provider.
        Returns a list of dictionaries with keys like 'title', 'body', 'href'.
        """
        pass
