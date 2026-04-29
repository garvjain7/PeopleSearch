import re
from typing import List, Tuple
from backend.models import CandidateProfile, ScoredExpert
from .weights import ROLE_SCORES, COMPANY_SCORES, TECH_DEPTH_KEYWORDS, DOMAIN_KEYWORDS

class Scorer:
    """
    Weighted Scoring Engine
    Final Score = 
      domain_score * 0.30 
      + role_score * 0.25 
      + company_score * 0.20 
      + technical_depth_score * 0.15 
      + network_quality_proxy * 0.10
    """
    
    @classmethod
    def score_profiles(cls, profiles: List[CandidateProfile], query: str) -> List[Tuple[CandidateProfile, float, dict]]:
        scored_results = []
        
        # Add query to domain keywords dynamically
        dynamic_domain = set(DOMAIN_KEYWORDS)
        for q_word in query.lower().split():
            if len(q_word) > 3:
                dynamic_domain.add(q_word)

        for p in profiles:
            text_context = f"{p.title} {p.snippet}".lower()
            
            # 1. Domain Score (out of 100)
            domain_hits = sum(1 for kw in dynamic_domain if kw in text_context)
            domain_score = min(100, domain_hits * 25) # 4 hits = 100
            
            # 2. Role Score (out of 100)
            role_score = 50 # Default baseline
            for role, score in ROLE_SCORES.items():
                if role in text_context:
                    role_score = score
                    break # Take the first match
            
            # 3. Company Score (out of 100)
            company_score = 50 # Default baseline
            if p.company:
                comp_lower = p.company.lower()
                for comp, score in COMPANY_SCORES.items():
                    if comp in comp_lower:
                        company_score = score
                        break
            
            # 4. Technical Depth Score (out of 100)
            tech_hits = sum(1 for kw in TECH_DEPTH_KEYWORDS if kw in text_context)
            technical_depth_score = min(100, tech_hits * 30) # ~3 hits = 90
            
            # 5. Network Quality Proxy (out of 100)
            # Proxy: Has a clean name, explicit company, and rich snippet
            network_quality = 50
            if len(p.snippet) > 50 and p.company != "Unknown":
                network_quality += 30
            if "..." not in p.name:
                network_quality += 20
                
            # Calculate Final Score
            final_score = (
                (domain_score * 0.30) +
                (role_score * 0.25) +
                (company_score * 0.20) +
                (technical_depth_score * 0.15) +
                (network_quality * 0.10)
            )
            
            breakdown = {
                "domain_score": domain_score,
                "role_score": role_score,
                "company_score": company_score,
                "technical_depth_score": technical_depth_score,
                "network_quality_proxy": network_quality
            }
            
            scored_results.append((p, final_score, breakdown))
            
        return scored_results
