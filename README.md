# LinkedIn Similar Expert Finder

A production-quality MVP for finding similar LinkedIn professionals based on domain relevance, role quality, company tier, and technical depth.

## Features

- **Candidate Discovery**: Leverages search engine abstractions to find profiles without depending on restricted APIs.
- **Intelligent Scoring**: A deterministic 100-point scoring system evaluating Domain, Role, Company, Technical Depth, and Network Quality.
- **Explainer Layer**: Generates human-readable explanations of exactly why a candidate matched the target criteria.
- **Resilient Backend**: FastAPI backend featuring explicit retry and rate-limit backoff mechanisms.
- **Professional UI**: A clean, "recruiter-grade" React/Vite interface.

## Project Structure

- `backend/`: FastAPI application containing Providers, Normalizers, Scoring, and Explainers.
- `frontend/`: React + Vite application containing the search interface and results visualization.

## Documentation

For a deep dive into the system's design and logic, please read the [Architecture Guide](ARCHITECTURE.md).

## Getting Started

### 1. Start the Backend
```bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Mac/Linux:
# source venv/bin/activate

pip install -r backend/requirements.txt
python -m backend.main
```
The backend will be available at `http://localhost:8000`.

### 2. Start the Frontend
Open a new terminal:
```bash
cd frontend
npm install
npm run dev
```
The frontend will be available at `http://localhost:5173`.
