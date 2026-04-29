import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from backend.services.expert_finder import ExpertFinderService

service = ExpertFinderService()
experts = service.find_experts("RAG Engineer", "AI Infrastructure")
print(f"Found {len(experts)} experts:")
for e in experts:
    print(f"- {e.profile.name} at {e.profile.company}: Score {e.score} ({e.reason})")
