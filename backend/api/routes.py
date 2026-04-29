from fastapi import APIRouter, HTTPException
from backend.models import SearchRequest, SearchResponse
from backend.services.expert_finder import ExpertFinderService

router = APIRouter()
expert_service = ExpertFinderService()

@router.post("/experts/find", response_model=SearchResponse)
async def find_experts(request: SearchRequest):
    try:
        experts = expert_service.find_experts(request.query, request.domain)
        return SearchResponse(
            count=len(experts),
            experts=experts
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    return {"status": "healthy"}

@router.get("/providers")
async def list_providers():
    return {
        "active": "duckduckgo",
        "available": ["duckduckgo", "serpapi (planned)", "google (planned)"]
    }
