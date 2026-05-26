from __future__ import annotations

import re

from .models import SearchProfile

SKILL_ALIASES = {
    "ai": "AI",
    "llm": "LLM",
    "large language model": "LLM",
    "rag": "RAG",
    "retrieval augmented generation": "RAG",
    "python": "Python",
    "postgres": "PostgreSQL",
    "postgresql": "PostgreSQL",
    "pgvector": "Vector Search",
    "vector": "Vector Search",
    "semantic search": "Vector Search",
    "search": "Search",
    "fastapi": "FastAPI",
    "async": "AsyncIO",
    "asyncio": "AsyncIO",
    "docker": "Docker",
    "alembic": "Alembic",
    "playwright": "Playwright",
    "browser": "Browser Automation",
    "crawler": "Crawling",
    "crawling": "Crawling",
    "github": "GitHub API",
    "semantic scholar": "Semantic Scholar",
    "openalex": "OpenAlex",
    "nlp": "NLP",
    "pytorch": "PyTorch",
    "sql": "SQL",
    "crm": "CRM",
    "testing": "Testing",
    "mypy": "Mypy",
    "typescript": "TypeScript",
}

ROLE_HINTS = {
    "research": "Research",
    "scientist": "Research",
    "engineer": "Engineering",
    "backend": "Backend",
    "platform": "Platform",
    "product": "Product",
    "recruit": "Recruiting",
    "talent": "Talent Intelligence",
    "lead": "Leadership",
    "principal": "Leadership",
    "staff": "Leadership",
}

SENIORITY_HINTS = {
    "junior": 2,
    "mid": 4,
    "senior": 7,
    "staff": 9,
    "principal": 11,
    "lead": 8,
    "head": 10,
}

KNOWN_LANGUAGES = ["English", "Mandarin", "Japanese", "Spanish", "German", "Portuguese"]
KNOWN_LOCATIONS = ["US", "Canada", "Germany", "Portugal", "Japan", "Spain", "Remote", "Hong Kong"]


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def unique(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        key = item.lower()
        if key not in seen:
            seen.add(key)
            result.append(item)
    return result


class DeterministicJDParser:
    """Deterministic parser used by the Python tool layer.

    In the intended product, Claude Code can provide higher-level judgment before
    calling this parser. This parser remains predictable and testable.
    """

    def parse(self, text: str) -> SearchProfile:
        lowered = normalize(text)
        skills = [
            canonical
            for needle, canonical in SKILL_ALIASES.items()
            if re.search(rf"\b{re.escape(needle)}\b", lowered)
        ]
        role_hints = [
            canonical
            for needle, canonical in ROLE_HINTS.items()
            if re.search(rf"\b{re.escape(needle)}\b", lowered)
        ]
        languages = [language for language in KNOWN_LANGUAGES if language.lower() in lowered]
        locations = [location for location in KNOWN_LOCATIONS if location.lower() in lowered]
        explicit_years = [int(value) for value in re.findall(r"(\d+)\+?\s*(?:years|yrs)", lowered)]
        hinted_years = [years for hint, years in SENIORITY_HINTS.items() if hint in lowered]
        minimum_years = max(explicit_years + hinted_years + [0])

        return SearchProfile(
            raw_text=text,
            skills=unique(skills),
            role_hints=unique(role_hints),
            languages=unique(languages),
            locations=unique(locations),
            minimum_years=minimum_years,
            wants_research=any(word in lowered for word in ["phd", "paper", "publication", "research", "citation"]),
            wants_leadership=any(word in lowered for word in ["lead", "manager", "staff", "principal", "mentor"]),
        )

