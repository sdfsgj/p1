from __future__ import annotations

from oculai.models import Candidate, SearchProfile


class BrowserProfileSource:
    name = "browser_profiles"

    async def search(self, profile: SearchProfile, limit: int) -> list[Candidate]:
        raise NotImplementedError(
            "Browser enrichment should be implemented with Patchright, Camoufox, or Crawl4AI in an isolated worker."
        )

