from __future__ import annotations

import math

from .embedding import HashingEmbedder, cosine_similarity
from .models import Candidate, CandidateEvaluation, SearchProfile


def overlap_score(required: list[str], offered: list[str]) -> tuple[float, list[str]]:
    if not required:
        return 0.65, []
    offered_lower = {item.lower(): item for item in offered}
    matched = [skill for skill in required if skill.lower() in offered_lower]
    return len(matched) / len(required), matched


def bounded_log(value: float, base: float) -> float:
    return min(1.0, math.log(value + 1, base))


class CandidateScorer:
    def __init__(self, embedder: HashingEmbedder | None = None) -> None:
        self.embedder = embedder or HashingEmbedder()

    def score(self, profile: SearchProfile, candidate: Candidate) -> CandidateEvaluation:
        skill_score, matched_skills = overlap_score(profile.skills, candidate.skills)
        role_score, matched_domains = overlap_score(profile.role_hints, candidate.domains + [candidate.title])
        research_score = (bounded_log(candidate.citations, 5000) * 0.55) + (
            min(candidate.h_index, 25) / 25 * 0.45
        )
        engineering_score = (bounded_log(candidate.github_stars, 8000) * 0.45) + (
            min(candidate.years_experience, 12) / 12 * 0.55
        )
        leadership_score = candidate.leadership / 5
        years_score = (
            1.0
            if candidate.years_experience >= profile.minimum_years
            else candidate.years_experience / max(profile.minimum_years, 1)
        )
        semantic_score = self._semantic_score(profile, candidate)

        weights = {
            "skills": 0.26,
            "semantic": 0.12,
            "role": 0.1,
            "research": 0.14 if profile.wants_research else 0.08,
            "engineering": 0.16,
            "leadership": 0.12 if profile.wants_leadership else 0.07,
            "language": 0.07,
            "location": 0.07,
            "years": 0.06,
        }
        total_weight = sum(weights.values())
        weighted = (
            skill_score * weights["skills"]
            + semantic_score * weights["semantic"]
            + role_score * weights["role"]
            + research_score * weights["research"]
            + engineering_score * weights["engineering"]
            + leadership_score * weights["leadership"]
            + self._language_score(profile, candidate) * weights["language"]
            + self._location_score(profile, candidate) * weights["location"]
            + years_score * weights["years"]
        ) / total_weight

        return CandidateEvaluation(
            candidate=candidate,
            score=round(weighted * 100),
            matched_skills=matched_skills,
            matched_domains=matched_domains,
            reasons=self._build_reasons(profile, candidate, matched_skills, matched_domains),
            outreach=self._build_outreach(candidate, matched_skills),
            scores={
                "skills": round(skill_score * 100),
                "semantic": round(semantic_score * 100),
                "role": round(role_score * 100),
                "research": round(research_score * 100),
                "engineering": round(engineering_score * 100),
                "leadership": round(leadership_score * 100),
                "language": round(self._language_score(profile, candidate) * 100),
                "location": round(self._location_score(profile, candidate) * 100),
                "seniority": round(years_score * 100),
            },
        )

    def _semantic_score(self, profile: SearchProfile, candidate: Candidate) -> float:
        candidate_text = " ".join([candidate.title, *candidate.skills, *candidate.domains, *candidate.signals])
        raw = cosine_similarity(self.embedder.embed(profile.raw_text), self.embedder.embed(candidate_text))
        return max(0.0, min(1.0, (raw + 1.0) / 2.0))

    @staticmethod
    def _location_score(profile: SearchProfile, candidate: Candidate) -> float:
        if not profile.locations:
            return 0.72
        candidate_location = candidate.location.lower()
        return 1.0 if any(location.lower() in candidate_location for location in profile.locations) else 0.35

    @staticmethod
    def _language_score(profile: SearchProfile, candidate: Candidate) -> float:
        if not profile.languages:
            return 0.75
        candidate_languages = {item.lower() for item in candidate.languages}
        matched = [item for item in profile.languages if item.lower() in candidate_languages]
        return len(matched) / len(profile.languages)

    @staticmethod
    def _build_reasons(
        profile: SearchProfile,
        candidate: Candidate,
        matched_skills: list[str],
        matched_domains: list[str],
    ) -> list[str]:
        reasons = []
        if matched_skills:
            reasons.append(f"Matches key skills: {', '.join(matched_skills[:5])}.")
        if matched_domains:
            reasons.append(f"Relevant role/domain signal: {', '.join(matched_domains[:3])}.")
        if profile.wants_research and candidate.h_index >= 10:
            reasons.append(f"Strong academic footprint with h-index {candidate.h_index} and {candidate.citations} citations.")
        if profile.wants_leadership and candidate.leadership >= 4:
            reasons.append("Clear leadership signal from senior ownership and team guidance.")
        if candidate.signals:
            reasons.append(candidate.signals[0])
        return reasons[:4]

    @staticmethod
    def _build_outreach(candidate: Candidate, matched_skills: list[str]) -> str:
        skill_line = ", ".join(matched_skills[:3]) if matched_skills else candidate.domains[0]
        return (
            f"Hi {candidate.name.split()[0]}, I came across your work around {skill_line} and thought it lined up "
            "with a role building AI-native talent intelligence systems. The team is looking for someone who can "
            "connect deep technical judgment with practical recruiting workflows. Would you be open to a short conversation?"
        )

