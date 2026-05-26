from __future__ import annotations

from urllib.parse import quote_plus

from oculai.models import Candidate, SearchProfile


class ArxivSource:
    name = "arxiv"

    def build_search_url(self, profile: SearchProfile, limit: int) -> str:
        query = quote_plus(" ".join(profile.skills + profile.role_hints) or "machine learning")
        return (
            "https://export.arxiv.org/api/query"
            f"?search_query=all:{query}&start=0&max_results={limit}&sortBy=relevance&sortOrder=descending"
        )

    async def search(self, profile: SearchProfile, limit: int) -> list[Candidate]:
        raise NotImplementedError("arXiv OAI/API fetching is the next production integration step.")

