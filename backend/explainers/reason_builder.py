from typing import Dict, Any

class ReasonBuilder:
    @staticmethod
    def build_reason(breakdown: Dict[str, float], company: str, title: str) -> str:
        """
        Generates human-readable explanations based on the scoring breakdown.
        """
        reasons = []
        
        # Company Reason
        if breakdown['company_score'] >= 90:
            reasons.append(f"Works at top-tier company ({company}).")
        elif company and company != "Unknown":
            reasons.append(f"Currently at {company}.")
            
        # Role Reason
        if breakdown['role_score'] >= 90:
            reasons.append(f"Role strongly matches target engineering profile.")
        elif breakdown['role_score'] < 50:
            reasons.append(f"Role might be less technical.")
            
        # Domain & Tech Depth Reason
        if breakdown['technical_depth_score'] >= 60 and breakdown['domain_score'] >= 50:
            reasons.append(f"Snippet indicates strong technical implementation experience and domain overlap.")
        elif breakdown['domain_score'] >= 75:
            reasons.append(f"High keyword overlap with target domain.")
        elif breakdown['technical_depth_score'] >= 60:
            reasons.append(f"Mentions production/scaling experience.")
            
        if not reasons:
            return "General domain match based on search heuristics."
            
        return " ".join(reasons)
