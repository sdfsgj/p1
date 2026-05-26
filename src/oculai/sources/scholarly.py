from __future__ import annotations

from urllib.parse import quote_plus

from oculai.models import Candidate, SearchProfile


class SemanticScholarSource:
    name = "semantic_scholar"

    def build_search_url(self, profile: SearchProfile, limit: int) -> str:
        query = quote_plus(" ".join(profile.skills + profile.role_hints) or "machine learning")
        return f"https://api.semanticscholar.org/graph/v1/paper/search?query={query}&limit={limit}"

    async def search(self, profile: SearchProfile, limit: int) -> list[Candidate]:
        raise NotImplementedError("Semantic Scholar HTTP fetching is the next production integration step.")


class OpenAlexSource:
    name = "openalex"

    def build_search_url(self, profile: SearchProfile, limit: int) -> str:
        query = quote_plus(" ".join(profile.skills + profile.role_hints) or "machine learning")
        return f"https://api.openalex.org/works?search={query}&per-page={limit}"

    async def search(self, profile: SearchProfile, limit: int) -> list[Candidate]:
        raise NotImplementedError("OpenAlex HTTP fetching is the next production integration step.")

