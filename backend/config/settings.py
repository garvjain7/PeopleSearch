import os

class Settings:
    # Minimum score required to be returned in results (out of 100)
    MIN_ACCEPTABLE_SCORE = 60
    
    # Max number of experts to return
    MAX_RESULTS = 50
    
    # Request limits
    MAX_SEARCH_PAGES = 5
    
    # Optional Provider API keys
    SERPAPI_KEY = os.getenv("SERPAPI_KEY", "")

settings = Settings()
