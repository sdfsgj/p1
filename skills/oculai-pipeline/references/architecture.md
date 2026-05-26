# Oculai Architecture Reference

## Core Principle

Claude Code is the decision layer. Python code should expose deterministic functions and adapters:

- Parse JD signals into a structured `SearchProfile`.
- Fetch or load candidate data.
- Embed, filter, rank, and score candidates.
- Persist runs, candidates, evaluations, and outreach events.
- Serve API responses and the dashboard.

## Main Modules

- `models.py`: dataclasses for `SearchProfile`, `Candidate`, `CandidateEvaluation`, and `PipelinePhase`.
- `jd_parser.py`: deterministic keyword and metadata extraction from JD text.
- `embedding.py`: local fallback embedding plus cosine similarity.
- `scoring.py`: ranking model and explainability fields.
- `repositories.py`: local JSON repository for offline development.
- `postgres_repository.py`: production PostgreSQL repository boundary.
- `pipeline.py`: orchestrates parse, candidate load/search, scoring, and response assembly.
- `sources/`: external candidate source adapters.

## Database

Use PostgreSQL with:

- `vector` for embedding storage.
- `pg_trgm` for fuzzy name/text search.
- `uuid-ossp` for UUID primary keys.

Important tables:

- `search_runs`: JD, parsed profile, run status.
- `candidates`: normalized candidate records with source metadata and optional vector.
- `candidate_evaluations`: run-specific candidate scores, reasons, and outreach drafts.
- `outreach_events`: closed-loop tracking of contact attempts and responses.

## Production Direction

Local JSON is only a development seed. For production, build the pipeline around PostgreSQL and run external source ingestion before ranking.

