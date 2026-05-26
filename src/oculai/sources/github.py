from __future__ import annotations

from urllib.parse import quote_plus

from oculai.models import Candidate, SearchProfile


class GitHubSource:
    name = "github"

    def build_search_url(self, profile: SearchProfile, limit: int) -> str:
        skills = " ".join(profile.skills[:4]) or "python"
        query = quote_plus(f"{skills} in:readme stars:>20")
        return f"https://api.github.com/search/repositories?q={query}&per_page={limit}"

    async def search(self, profile: SearchProfile, limit: int) -> list[Candidate]:
        raise NotImplementedError(
            "GitHubSource is wired as an adapter boundary. Connect it with httpx and a GitHub token before production use."
        )

