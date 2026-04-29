import logging
from typing import List, Optional
from backend.providers.duckduckgo import DuckDuckGoProvider
from backend.scraping.parser import ProfileParser
from backend.normalizers.profile_normalizer import ProfileNormalizer
from backend.ranking.scorer import Scorer
from backend.explainers.reason_builder import ReasonBuilder
from backend.models import ScoredExpert
from backend.config.settings import settings

logger = logging.getLogger(__name__)

class ExpertFinderService:
    def __init__(self):
        # MVP uses DuckDuckGo by default
        self.provider = DuckDuckGoProvider()

    def find_experts(self, query: str, domain: Optional[str] = None) -> List[ScoredExpert]:
        """
        Orchestrates the discovery, parsing, normalization, scoring, and explaining pipeline.
        """
        # Combine query with domain if provided
        full_query = f"{query} {domain}" if domain else query
        
        logger.info(f"Starting discovery for query: {full_query}")
        
        # 1. Discover Candidates
        raw_results = self.provider.search_linkedin(full_query, max_results=settings.MAX_RESULTS * 2)
        if not raw_results:
            logger.warning("No results returned from provider.")
            return []
            
        # 2. Parse Results
        profiles = ProfileParser.parse_search_results(raw_results)
        
        # 3. Normalize & Deduplicate
        normalized_profiles = ProfileNormalizer.normalize_profiles(profiles)
        
        # 4. Score Profiles
        scored_results = Scorer.score_profiles(normalized_profiles, full_query)
        
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
        return final_experts[:settings.MAX_RESULTS]
