# Oculai Data Sources Reference

## Source Adapter Pattern

Each adapter should live under `src/oculai/sources/` and expose:

```python
name = "source_name"

async def search(profile: SearchProfile, limit: int) -> list[Candidate]:
    ...
```

Use stable `source` and `source_id` values so records can be upserted safely.

## Supported Sources

- GitHub REST API: repositories, contributors, user profiles, stars, languages, open source signals.
- arXiv: papers and authors for research discovery.
- DBLP: CS publication metadata.
- Semantic Scholar: papers, authors, citations, h-index, ORCID, affiliations.
- OpenAlex: open academic graph across works, authors, institutions, and topics.
- Browser enrichment: Google Scholar, public profiles, personal sites, and pages without reliable APIs.

## Integration Requirements

- Use `httpx` with configured timeout.
- Keep rate limits and pagination explicit.
- Retain `raw_payload` for audit and later enrichment.
- Normalize source records into `Candidate`.
- Add tests for query construction and payload mapping.
- Avoid making scoring depend on provider-specific raw fields.

## Browser Enrichment

Use browser automation only in a dedicated source/enrichment adapter. Keep it separate from the core ranking path so the system can still run with API-only data.

