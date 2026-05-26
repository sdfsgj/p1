from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    database_url: str = "postgresql://oculai:oculai@localhost:5432/oculai"
    github_token: str = ""
    semantic_scholar_key: str = ""
    http_timeout_seconds: float = 20.0
    embedding_model: str = "all-MiniLM-L6-v2"


def load_settings() -> Settings:
    return Settings(
        database_url=os.getenv("OCULAI_DATABASE_URL", Settings.database_url),
        github_token=os.getenv("OCULAI_GITHUB_TOKEN", ""),
        semantic_scholar_key=os.getenv("OCULAI_SEMANTIC_SCHOLAR_KEY", ""),
        http_timeout_seconds=float(os.getenv("OCULAI_HTTP_TIMEOUT_SECONDS", "20")),
        embedding_model=os.getenv("OCULAI_EMBEDDING_MODEL", Settings.embedding_model),
    )

