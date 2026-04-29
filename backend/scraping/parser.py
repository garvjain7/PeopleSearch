import re
from typing import List, Dict, Any
from backend.models import CandidateProfile
import logging

logger = logging.getLogger(__name__)

class ProfileParser:
    @staticmethod
    def parse_search_results(raw_results: List[Dict[str, Any]]) -> List[CandidateProfile]:
        """
        Parses raw search engine results into CandidateProfile models.
        Handles malformed snippets and invalid URLs.
        """
        profiles = []
        for res in raw_results:
            title = res.get('title', '')
            snippet = res.get('body', '')
            url = res.get('href', '')
            
            # Ensure valid linkedin /in/ URL
            if not url or '/in/' not in url:
                continue
                
            # Title usually looks like: "John Doe - Machine Learning Engineer - OpenAI | LinkedIn"
            # We want to extract Name and Role/Company if possible
            clean_title = re.sub(r'\s*\|\s*LinkedIn\s*', '', title)
            
            # Very naive split, normalizer will fix it later
            parts = [p.strip() for p in clean_title.split('-')]
            
            name = parts[0] if len(parts) > 0 else "Unknown"
            
            # If name has "..." or looks truncated, we still keep it but might penalize later
            
            # Fallback for role
            role = parts[1] if len(parts) > 1 else ""
            
            profile = CandidateProfile(
                name=name,
                title=role or clean_title,
                snippet=snippet,
                url=url
            )
            profiles.append(profile)
            
        logger.info(f"Parsed {len(profiles)} profiles from search results.")
        return profiles
