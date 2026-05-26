from __future__ import annotations

import json
from pathlib import Path
from typing import Protocol

from .models import Candidate


class CandidateRepository(Protocol):
    def list_candidates(self) -> list[Candidate]:
        ...

    def upsert_many(self, candidates: list[Candidate]) -> None:
        ...


class JsonCandidateRepository:
    def __init__(self, path: Path) -> None:
        self.path = path

    def list_candidates(self) -> list[Candidate]:
        with self.path.open("r", encoding="utf-8") as file:
            payload = json.load(file)
        return [Candidate.from_dict(item) for item in payload]

    def upsert_many(self, candidates: list[Candidate]) -> None:
        existing = {candidate.id: candidate for candidate in self.list_candidates()}
        for candidate in candidates:
            existing[candidate.id] = candidate
        with self.path.open("w", encoding="utf-8") as file:
            json.dump([candidate.to_dict() for candidate in existing.values()], file, ensure_ascii=False, indent=2)

