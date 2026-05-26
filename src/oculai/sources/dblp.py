from __future__ import annotations

from urllib.parse import quote_plus

from oculai.models import Candidate, SearchProfile


class DblpSource:
    name = "dblp"

    def build_search_url(self, profile: SearchProfile, limit: int) -> str:
        query = quote_plus(" ".join(profile.skills + profile.role_hints) or "machine learning")
        return f"https://dblp.org/search/publ/api?q={query}&format=json&h={limit}"

    async def search(self, profile: SearchProfile, limit: int) -> list[Candidate]:
        raise NotImplementedError("DBLP fetching is the next production integration step.")

