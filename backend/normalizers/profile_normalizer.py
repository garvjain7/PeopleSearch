import re
from typing import List, Tuple
from backend.models import CandidateProfile

class ProfileNormalizer:
    
    # Common company names we want to exact match if they appear
    KNOWN_COMPANIES = [
        "OpenAI", "Anthropic", "Google", "DeepMind", "Meta", "Facebook",
        "Pinecone", "Weaviate", "Qdrant", "Milvus", "Databricks", "Snowflake",
        "LangChain", "LlamaIndex", "NVIDIA", "MongoDB", "AWS", "Amazon",
        "Microsoft", "Cohere", "Hugging Face"
    ]

    @classmethod
    def normalize_profiles(cls, profiles: List[CandidateProfile]) -> List[CandidateProfile]:
        """
        Cleans titles, extracts companies, and removes duplicates by URL.
        """
        seen_urls = set()
        unique_profiles = []
        
        for p in profiles:
            # 1. URL Normalization & Deduplication
            # Remove any trailing query params
            clean_url = p.url.split('?')[0].rstrip('/')
            if clean_url in seen_urls:
                continue
            seen_urls.add(clean_url)
            p.url = clean_url
            
            # 2. Extract company
            extracted_company = cls._extract_company(p.title, p.snippet)
            p.company = extracted_company
            
            # 3. Clean Title
            p.title = cls._clean_title(p.title)
            
            # 4. Clean Name
            p.name = cls._clean_name(p.name)
            
            unique_profiles.append(p)
            
        return unique_profiles

    @classmethod
    def _extract_company(cls, title: str, snippet: str) -> str:
        text_to_search = f"{title} {snippet}"
        
        # Look for known top-tier companies first
        for company in cls.KNOWN_COMPANIES:
            # simple case insensitive search
            if re.search(rf"\b{company}\b", text_to_search, re.IGNORECASE):
                return company
                
        # Heuristic: look for "at [Company]"
        at_match = re.search(r'\bat\s+([A-Z][a-zA-Z0-9&\-\s]+)(?:\W|$)', text_to_search)
        if at_match:
            candidate = at_match.group(1).strip()
            # simple heuristic to avoid long sentences
            if len(candidate.split()) <= 3:
                return candidate
                
        return "Unknown"

    @classmethod
    def _clean_title(cls, title: str) -> str:
        # Remove noisy words
        noise = [" at ", "...", " | LinkedIn", "Profile"]
        for n in noise:
            title = title.replace(n, " ")
        
        # Remove excessive whitespace
        title = re.sub(r'\s+', ' ', title).strip()
        return title

    @classmethod
    def _clean_name(cls, name: str) -> str:
        # Remove anything after a comma, dash or pipe in the name
        name = re.split(r'[,-|]', name)[0].strip()
        # Remove academic titles or certifications (e.g. Ph.D.)
        name = re.sub(r'\b(PhD|Ph\.D\.|MSc|BSc)\b', '', name, flags=re.IGNORECASE)
        return re.sub(r'\s+', ' ', name).strip()
