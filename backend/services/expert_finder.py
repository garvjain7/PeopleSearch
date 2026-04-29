import logging
from typing import List, Optional
from backend.providers.duckduckgo import DuckDuckGoProvider
from backend.providers.serpapi import SerpAPIProvider
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
        # MVP Primary Provider
        self.provider = DuckDuckGoProvider()
        # Real Production Fallback Provider
        self.fallback_provider = SerpAPIProvider()

    def _format_query(self, query: str, domain: Optional[str]) -> str:
        """
        Transforms weak queries into proper quoted search terms.
        """
        query_parts = [p.strip() for p in query.split('/')] if query else []
        domain_parts = [p.strip() for p in domain.split('/')] if domain else []
        
        all_parts = query_parts + domain_parts
        # Wrap each part in quotes to enforce exact/stronger matching
        formatted_query = " ".join([f'"{p}"' for p in all_parts if p])
        return formatted_query

    def find_experts(self, query: str, domain: Optional[str] = None) -> List[ScoredExpert]:
        full_query = self._format_query(query, domain)
        logger.info(f"Starting discovery for formatted query: {full_query}")
        
        # Check Cache
        cache_key = full_query.lower()
        if cache_key in _search_cache:
            logger.info("Returning cached results to avoid duplicate request.")
            return _search_cache[cache_key]
        
        # 1. Discover Candidates
        raw_results = self.provider.search_linkedin(full_query, max_results=settings.MAX_RESULTS * 2)
        
        # 1.5 Fallback Architecture
        if raw_results is None:
            logger.warning("Primary provider failed. Triggering SerpAPI fallback.")
            raw_results = self.fallback_provider.search_linkedin(full_query, max_results=settings.MAX_RESULTS * 2)
            
        if raw_results is None:
            logger.error("All providers failed or rate-limited.")
            raise ValueError("Search providers are currently rate-limited. Please try again in a few minutes or configure a SerpAPI key.")
            
        if not raw_results:
            logger.info("Search succeeded but found 0 results.")
            return []
            
        # 2. Parse Results
        profiles = ProfileParser.parse_search_results(raw_results)
        
        # 3. Normalize & Deduplicate
        normalized_profiles = ProfileNormalizer.normalize_profiles(profiles)
        
        # 4. Score Profiles
        # Pass the unquoted raw string to the scorer so keyword matching still works smoothly
        raw_context_query = f"{query} {domain}" if domain else query
        scored_results = Scorer.score_profiles(normalized_profiles, raw_context_query)
        
        # 5. Filter, Explain, and Format
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
                
        # 6. Sort by score descending and limit to MAX_RESULTS
        final_experts.sort(key=lambda x: x.score, reverse=True)
        final_results = final_experts[:settings.MAX_RESULTS]
        
        # Store in cache
        _search_cache[cache_key] = final_results
        
        return final_results
