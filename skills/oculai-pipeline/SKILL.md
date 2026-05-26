---
name: oculai-pipeline
description: Build, extend, deploy, or troubleshoot the Oculai AI-native talent sourcing pipeline. Use when working on Oculai project code, recruiting pipeline architecture, JD parsing, candidate sourcing, PostgreSQL/pgvector schema, external source adapters such as GitHub/arXiv/DBLP/Semantic Scholar/OpenAlex, browser-based candidate enrichment, candidate ranking/scoring, outreach drafting, cloud deployment, or GitHub/Render setup for the Oculai repository.
---

# Oculai Pipeline

## Overview

Use this skill to work on Oculai as a real project, not as a throwaway demo. Preserve the architecture principle: Claude Code makes orchestration and judgment calls; Python exposes deterministic tools for parsing, data access, ranking, enrichment, storage, and API serving.

## First Steps

1. Inspect the repository before editing: run `rg --files`, read `README.md`, `server.py`, and relevant files under `src/oculai/`.
2. Identify whether the task is about architecture, data sources, scoring, persistence, UI, deployment, or GitHub workflow.
3. Use the closest existing module rather than rebuilding the flow in one file.
4. Run `python -m unittest discover -s tests` after code changes.
5. If the task touches project completeness, run `scripts/check_oculai_project.py <repo-root>`.

## Architecture Rules

- Keep domain logic in `src/oculai/`, with the local HTTP entry point in `server.py`.
- Keep deterministic JD parsing in `jd_parser.py`; do not call LLM APIs from Python utility code.
- Keep candidate ranking in `scoring.py`; explain scores with structured fields, not only prose.
- Keep candidate storage behind repositories. Use JSON only for local development; use PostgreSQL/pgvector for production.
- Keep source integrations under `src/oculai/sources/`; each source should expose a clear adapter boundary.
- Keep browser automation as an isolated enrichment/source layer; never mix scraping logic into scoring.
- Preserve `web/` as the local operational dashboard unless the user asks for a frontend framework migration.

## Task Routing

- For database or schema work, read `references/architecture.md`.
- For source integrations, read `references/data-sources.md`.
- For cloud deployment, GitHub upload, Render, or environment variables, read `references/deployment.md`.
- For quick structural validation, run `scripts/check_oculai_project.py`.

## Expected Project Shape

The repository should generally include:

```text
server.py
README.md
requirements.txt
pyproject.toml
docker-compose.yml
render.yaml
Procfile
data/candidates.json
sql/001_initial_schema.sql
src/oculai/
src/oculai/sources/
tests/
web/
```

## Implementation Guidance

- Prefer small, testable additions: add an adapter, repository method, scoring dimension, or API endpoint in the appropriate module.
- Keep local development usable without network access or API keys.
- When adding live external APIs, include timeouts, pagination limits, source IDs, raw payload retention, and tests for URL/query construction.
- When adding PostgreSQL behavior, keep schema and repository code synchronized.
- When changing cloud deployment behavior, update both `README.md` and deployment files.

