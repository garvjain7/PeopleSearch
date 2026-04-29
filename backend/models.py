from pydantic import BaseModel, HttpUrl
from typing import List, Optional

class CandidateProfile(BaseModel):
    name: str
    title: str
    company: Optional[str] = None
    snippet: str
    url: str
    image_url: Optional[str] = None

class ScoredExpert(BaseModel):
    profile: CandidateProfile
    score: float
    reason: str
    domain_score: float
    role_score: float
    company_score: float
    technical_depth_score: float
    network_quality_proxy: float

class SearchRequest(BaseModel):
    query: str
    domain: Optional[str] = None

class SearchResponse(BaseModel):
    count: int
    experts: List[ScoredExpert]
