# Architecture Overview

The LinkedIn Similar Expert Finder is built with a highly decoupled, modular architecture designed for stability, explainability, and future scalability.

## Backend Architecture (FastAPI)

The backend is organized into distinct layers, each handling a specific responsibility in the data pipeline.

### 1. Providers Layer (`backend/providers/`)
The system abstracts search engines via the `SearchProvider` base class. 
- **MVP Implementation**: `DuckDuckGoProvider` is used for free, no-key candidate discovery.
- **Future Proofing**: Can easily swap to `SerpAPIProvider` or `GoogleProvider` by implementing the base interface.
- **Resilience**: Handled via `utils/retry.py` using exponential backoff to handle rate limits gracefully.

### 2. Scraping Layer (`backend/scraping/`)
- `parser.py`: Takes raw search engine JSON and converts it into structured `CandidateProfile` Pydantic models. Extracts basic names, URLs, and text snippets.

### 3. Normalization Layer (`backend/normalizers/`)
- `profile_normalizer.py`: Search data is highly noisy. The normalizer cleans up job titles (removing trailing " | LinkedIn" noise), deduplicates profiles by normalizing URLs, and heuristically extracts the candidate's current company.

### 4. Intelligence Layer (`backend/ranking/`)
This is the core product value. It avoids simple keyword matching in favor of a weighted scoring engine out of 100 points.
- **Domain Score (30%)**: Matches against query terms and target domains (e.g., "RAG", "Vector DB").
- **Role Score (25%)**: Maps roles to specific weights (e.g., "AI Engineer" = 100, "Influencer" = -50).
- **Company Score (20%)**: Grants multipliers for top-tier companies (e.g., OpenAI, Pinecone).
- **Technical Depth (15%)**: Scans for signals of real-world implementation ("scale", "production", "latency").
- **Network Quality (10%)**: A proxy score favoring profiles with clean data and rich snippets.
- **Quality Threshold**: Candidates scoring below `60` are automatically discarded.

### 5. Explainers Layer (`backend/explainers/`)
- `reason_builder.py`: A decoupled logic module that looks at the score breakdown and builds a human-readable sentence explaining the match (e.g., "Works at top-tier company. Mentions production/scaling experience.").

### 6. Services & API (`backend/services/` & `backend/api/`)
- `expert_finder.py`: Orchestrates the flow from Provider -> Parser -> Normalizer -> Scorer -> Explainer.
- `routes.py`: Exposes a clean `POST /api/v1/experts/find` endpoint.

---

## Frontend Architecture (React + Vite)

The frontend is a lightweight SPA (Single Page Application) focused on a professional, high-signal UI.

- **Component Driven**: Split into `SearchBar`, `ExpertCard`, and `ResultsList`.
- **Vanilla CSS**: Uses CSS variables for theming, delivering an enterprise-grade aesthetic without heavy frameworks.
- **Asynchronous Flow**: Uses simple `fetch` logic mapped to the backend endpoint, handling loading states and errors robustly.
