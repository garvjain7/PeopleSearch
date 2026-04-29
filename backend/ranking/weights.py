# backend/ranking/weights.py

# Role mappings to score (0 to 100 max)
ROLE_SCORES = {
    "applied ai engineer": 100,
    "ml engineer": 95,
    "machine learning engineer": 95,
    "ai platform engineer": 90,
    "backend engineer": 85,
    "software engineer": 80,
    "llm systems engineer": 100,
    "genai architect": 100,
    "search infrastructure engineer": 95,
    "data scientist": 75,
    "founder": 70,
    "cto": 80,
    "researcher": 85,
    "research scientist": 90,
    # Negative / Low quality proxies
    "content creator": -50,
    "influencer": -50,
    "motivational": -50,
    "coach": -50,
    "enthusiast": -30
}

# Company multipliers (0 to 100 max)
COMPANY_SCORES = {
    "openai": 100,
    "anthropic": 100,
    "deepmind": 100,
    "google": 90,
    "meta": 90,
    "pinecone": 95,
    "weaviate": 95,
    "qdrant": 95,
    "databricks": 90,
    "snowflake": 90,
    "langchain": 95,
    "llamaindex": 95,
    "nvidia": 95,
    "cohere": 95,
    "hugging face": 95,
    "aws": 85,
    "microsoft": 85
}

# Technical depth keywords
TECH_DEPTH_KEYWORDS = [
    "production", "scale", "latency", "evaluation", "evals",
    "retrieval optimization", "hallucination", "system architecture",
    "distributed", "high-throughput", "optimization", "infrastructure",
    "kubernetes", "docker", "gcp", "aws", "performance"
]

DOMAIN_KEYWORDS = [
    "rag", "retrieval augmented generation", "vector db", "vector database",
    "llmops", "ai infra", "search systems", "backend systems", "llm",
    "large language models", "generative ai"
]
