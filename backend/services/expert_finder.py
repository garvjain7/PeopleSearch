import logging
from typing import List, Optional
from backend.providers.serpapi import SerpAPIProvider
from backend.providers.duckduckgo import DuckDuckGoProvider
from backend.scraping.parser import ProfileParser
from backend.normalizers.profile_normalizer import ProfileNormalizer
from backend.ranking.scorer import Scorer
from backend.explainers.reason_builder import ReasonBuilder
from backend.models import ScoredExpert
from backend.config.settings import settings

logger = logging.getLogger(__name__)

# Simple in-memory cache to avoid duplicate searches
_search_cache = {}

class ExpertFinderService:
    def __init__(self):
        self.provider = SerpAPIProvider()
        self.fallback_provider = DuckDuckGoProvider()

    def _format_query(self, query: str, domain: Optional[str]) -> str:
        """
        Builds a clean natural language query for site:linkedin.com/in searches.
        Avoids over-quoting which causes 0 results on both SerpAPI and DDG.
        """
        parts = [p.strip() for p in [query, domain] if p and p.strip()]
        return " ".join(parts)

    def find_experts(self, query: str, domain: Optional[str] = None) -> List[ScoredExpert]:
        full_query = self._format_query(query, domain)
        logger.info(f"Starting discovery for query: {full_query}")

        # Check cache
        cache_key = full_query.lower()
        if cache_key in _search_cache:
            logger.info("Returning cached results.")
            return _search_cache[cache_key]

        # 1. Primary: SerpAPI
        raw_results = self.provider.search_linkedin(full_query, max_results=settings.MAX_RESULTS * 2)

        # 2. Fallback: DuckDuckGo
        if not raw_results:
            logger.warning("SerpAPI returned no results. Triggering DuckDuckGo fallback.")
            raw_results = self.fallback_provider.search_linkedin(full_query, max_results=settings.MAX_RESULTS * 2)

        # 3. Both failed
        if not raw_results:
            logger.error("All providers returned no results.")
            raise ValueError("No results found. SerpAPI may be rate-limited and DDG fallback also returned nothing. Try again shortly.")

        # 4. Parse
        profiles = ProfileParser.parse_search_results(raw_results)

        # 5. Normalize & deduplicate
        normalized_profiles = ProfileNormalizer.normalize_profiles(profiles)

        # 6. Score — pass raw unquoted query for keyword matching
        raw_context_query = f"{query} {domain}" if domain else query
        scored_results = Scorer.score_profiles(normalized_profiles, raw_context_query)

        # 7. Filter, explain, format
        final_experts = []
        for profile, score, breakdown in scored_results:
            if score >= settings.MIN_ACCEPTABLE_SCORE:
                reason = ReasonBuilder.build_reason(breakdown, profile.company, profile.title)
                expert = ScoredExpert(
                    profile=profile,
                    score=round(score, 1),
                    reason=reason,
                    **breakdown
                )
                final_experts.append(expert)

        # 8. Sort and limit
        final_experts.sort(key=lambda x: x.score, reverse=True)
        final_results = final_experts[:settings.MAX_RESULTS]

        _search_cache[cache_key] = final_results
        return final_results