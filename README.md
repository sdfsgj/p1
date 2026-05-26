# Oculai

Oculai is an AI-native talent sourcing pipeline. It turns a job description into a structured talent profile, searches candidate sources, ranks candidates with hard filters and semantic signals, creates a research dossier, generates evaluation scores, drafts outreach, and prepares closed-loop tracking.

The Python layer is intentionally deterministic: it exposes parsing helpers, source adapters, ranking, storage, and API endpoints. Claude Code or another orchestrator should make higher-level decisions such as which sources to search, how to refine the JD, and how to review final outreach.

## Current Implementation

This repository now contains a production-shaped local implementation:

- `src/oculai/models.py` defines search profiles, candidates, evaluations, and pipeline phases.
- `src/oculai/jd_parser.py` extracts deterministic JD signals.
- `src/oculai/embedding.py` provides a local hashing embedder with the same interface expected from a sentence-transformers embedder.
- `src/oculai/scoring.py` ranks candidates with skill, semantic, role, research, engineering, leadership, language, location, and seniority signals.
- `src/oculai/pipeline.py` runs the end-to-end pipeline.
- `src/oculai/sources/` contains source adapter boundaries for GitHub, arXiv, DBLP, Semantic Scholar, OpenAlex, and browser-based profile enrichment.
- `src/oculai/postgres_repository.py` contains the async PostgreSQL repository boundary for production storage.
- `sql/001_initial_schema.sql` defines the PostgreSQL, pgvector, pg_trgm, and uuid-ossp schema.
- `docker-compose.yml` starts a pgvector-enabled PostgreSQL instance.
- `server.py` exposes a local HTTP API and serves the dashboard in `web/`.

The default local app still seeds candidates from `data/candidates.json` so development works without API keys or network access. The codebase is structured so that JSON storage can be replaced by PostgreSQL and source adapters can be connected to live APIs.

## Run Locally

```powershell
cd "C:\Users\Kevin Hong\Desktop\p1"
python server.py
```

Open:

```text
http://localhost:8000
```

## Deploy From GitHub

This repo includes cloud-friendly process files:

- `Procfile` for platforms that detect web processes.
- `render.yaml` for Render Blueprint deployments.
- `server.py` reads the platform-provided `PORT` environment variable and binds to `0.0.0.0`.

For Render:

1. Push this repository to GitHub.
2. In Render, choose `New` -> `Blueprint`.
3. Select the GitHub repository.
4. Render will use `render.yaml` and expose the web service after build.

## Run Tests

```powershell
python -m unittest discover -s tests
```

## PostgreSQL Setup

Start the database:

```powershell
docker compose up -d postgres
```

The initialization script enables:

- `vector`
- `pg_trgm`
- `uuid-ossp`

It also creates:

- `search_runs`
- `candidates`
- `candidate_evaluations`
- `outreach_events`

Copy `.env.example` to `.env` and fill in API keys before connecting live data sources.

## API

```http
GET /api/health
GET /api/candidates
POST /api/analyze
```

Example request:

```json
{
  "job_description": "We need a senior AI engineer with LLM, RAG, Python, PostgreSQL, and research experience.",
  "limit": 8
}
```

## Pipeline

1. Phase 0: Requirement parsing
2. Phase 1: Wide search
3. Phase 2: Semantic matching
4. Phase 3: Deep research
5. Phase 4: Evaluation scoring
6. Phase 5: Outreach strategy
7. Phase 6: Closed-loop tracking

## Next Production Steps

- Implement `PostgresCandidateRepository` with `asyncpg`.
- Connect `GitHubSource`, `SemanticScholarSource`, `OpenAlexSource`, `DblpSource`, and `ArxivSource` through `httpx`.
- Replace `HashingEmbedder` with a sentence-transformers implementation using `all-MiniLM-L6-v2`.
- Add browser automation adapters for Google Scholar and public profile enrichment.
- Persist run history, evaluations, outreach events, and feedback into PostgreSQL.
