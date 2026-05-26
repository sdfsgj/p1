from __future__ import annotations

from typing import Protocol

from oculai.models import Candidate, SearchProfile


class CandidateSource(Protocol):
    name: str

    async def search(self, profile: SearchProfile, limit: int) -> list[Candidate]:
        ...

