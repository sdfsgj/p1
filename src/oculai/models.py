from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class PhaseStatus(StrEnum):
    COMPLETE = "complete"
    READY = "ready"
    SIMULATED = "simulated"


@dataclass(frozen=True)
class SearchProfile:
    raw_text: str
    skills: list[str]
    role_hints: list[str]
    languages: list[str]
    locations: list[str]
    minimum_years: int
    wants_research: bool
    wants_leadership: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "skills": self.skills,
            "role_hints": self.role_hints,
            "languages": self.languages,
            "locations": self.locations,
            "minimum_years": self.minimum_years,
            "wants_research": self.wants_research,
            "wants_leadership": self.wants_leadership,
        }


@dataclass(frozen=True)
class Candidate:
    id: str
    name: str
    title: str
    location: str
    languages: list[str]
    skills: list[str]
    domains: list[str]
    education: str
    publications: int
    citations: int
    h_index: int
    github_stars: int
    leadership: int
    years_experience: int
    source: str = "seed"
    source_id: str = ""
    profile_url: str = ""
    signals: list[str] = field(default_factory=list)
    raw_payload: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "Candidate":
        return cls(
            id=str(payload.get("id") or payload.get("source_id") or payload["name"]),
            name=str(payload["name"]),
            title=str(payload.get("title", "")),
            location=str(payload.get("location", "")),
            languages=list(payload.get("languages", [])),
            skills=list(payload.get("skills", [])),
            domains=list(payload.get("domains", [])),
            education=str(payload.get("education", "")),
            publications=int(payload.get("publications", 0)),
            citations=int(payload.get("citations", 0)),
            h_index=int(payload.get("h_index", 0)),
            github_stars=int(payload.get("github_stars", 0)),
            leadership=int(payload.get("leadership", 0)),
            years_experience=int(payload.get("years_experience", 0)),
            source=str(payload.get("source", "seed")),
            source_id=str(payload.get("source_id", payload.get("id", ""))),
            profile_url=str(payload.get("profile_url", "")),
            signals=list(payload.get("signals", [])),
            raw_payload=dict(payload.get("raw_payload", {})),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "title": self.title,
            "location": self.location,
            "languages": self.languages,
            "skills": self.skills,
            "domains": self.domains,
            "education": self.education,
            "publications": self.publications,
            "citations": self.citations,
            "h_index": self.h_index,
            "github_stars": self.github_stars,
            "leadership": self.leadership,
            "years_experience": self.years_experience,
            "source": self.source,
            "source_id": self.source_id,
            "profile_url": self.profile_url,
            "signals": self.signals,
            "raw_payload": self.raw_payload,
        }


@dataclass(frozen=True)
class CandidateEvaluation:
    candidate: Candidate
    score: int
    scores: dict[str, int]
    matched_skills: list[str]
    matched_domains: list[str]
    reasons: list[str]
    outreach: str

    def to_dict(self) -> dict[str, Any]:
        return {
            **self.candidate.to_dict(),
            "score": self.score,
            "scores": self.scores,
            "matched_skills": self.matched_skills,
            "matched_domains": self.matched_domains,
            "reasons": self.reasons,
            "outreach": self.outreach,
        }


@dataclass(frozen=True)
class PipelinePhase:
    phase: str
    name: str
    status: PhaseStatus

    def to_dict(self) -> dict[str, str]:
        return {"phase": self.phase, "name": self.name, "status": self.status.value}

