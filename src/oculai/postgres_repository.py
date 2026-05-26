from __future__ import annotations

from typing import Any

from .models import Candidate


class PostgresCandidateRepository:
    """PostgreSQL repository boundary for the production storage layer.

    The import of asyncpg is intentionally lazy so the local no-install workflow
    keeps working while production deployments can use the real dependency.
    """

    def __init__(self, database_url: str) -> None:
        self.database_url = database_url

    async def list_candidates(self) -> list[Candidate]:
        asyncpg = await self._asyncpg()
        connection = await asyncpg.connect(self.database_url)
        try:
            rows = await connection.fetch(
                """
                SELECT
                  id::text,
                  source,
                  source_id,
                  full_name AS name,
                  title,
                  location,
                  languages,
                  skills,
                  domains,
                  education,
                  publications,
                  citations,
                  h_index,
                  github_stars,
                  leadership,
                  years_experience,
                  profile_url,
                  raw_payload
                FROM candidates
                ORDER BY updated_at DESC
                """
            )
            return [Candidate.from_dict(dict(row)) for row in rows]
        finally:
            await connection.close()

    async def upsert_many(self, candidates: list[Candidate]) -> None:
        asyncpg = await self._asyncpg()
        connection = await asyncpg.connect(self.database_url)
        try:
            async with connection.transaction():
                for candidate in candidates:
                    await connection.execute(
                        """
                        INSERT INTO candidates (
                          source, source_id, full_name, title, location, languages, skills, domains,
                          education, publications, citations, h_index, github_stars, leadership,
                          years_experience, profile_url, raw_payload, updated_at
                        )
                        VALUES (
                          $1, $2, $3, $4, $5, $6, $7, $8,
                          $9, $10, $11, $12, $13, $14,
                          $15, $16, $17::jsonb, now()
                        )
                        ON CONFLICT (source, source_id)
                        DO UPDATE SET
                          full_name = EXCLUDED.full_name,
                          title = EXCLUDED.title,
                          location = EXCLUDED.location,
                          languages = EXCLUDED.languages,
                          skills = EXCLUDED.skills,
                          domains = EXCLUDED.domains,
                          education = EXCLUDED.education,
                          publications = EXCLUDED.publications,
                          citations = EXCLUDED.citations,
                          h_index = EXCLUDED.h_index,
                          github_stars = EXCLUDED.github_stars,
                          leadership = EXCLUDED.leadership,
                          years_experience = EXCLUDED.years_experience,
                          profile_url = EXCLUDED.profile_url,
                          raw_payload = EXCLUDED.raw_payload,
                          updated_at = now()
                        """,
                        candidate.source,
                        candidate.source_id or candidate.id,
                        candidate.name,
                        candidate.title,
                        candidate.location,
                        candidate.languages,
                        candidate.skills,
                        candidate.domains,
                        candidate.education,
                        candidate.publications,
                        candidate.citations,
                        candidate.h_index,
                        candidate.github_stars,
                        candidate.leadership,
                        candidate.years_experience,
                        candidate.profile_url,
                        candidate.raw_payload,
                    )
        finally:
            await connection.close()

    @staticmethod
    async def _asyncpg() -> Any:
        import asyncpg

        return asyncpg

