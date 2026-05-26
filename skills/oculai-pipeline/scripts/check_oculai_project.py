from __future__ import annotations

import sys
from pathlib import Path


REQUIRED_PATHS = [
    "server.py",
    "README.md",
    "requirements.txt",
    "pyproject.toml",
    "docker-compose.yml",
    "render.yaml",
    "Procfile",
    "data/candidates.json",
    "sql/001_initial_schema.sql",
    "src/oculai/__init__.py",
    "src/oculai/models.py",
    "src/oculai/jd_parser.py",
    "src/oculai/embedding.py",
    "src/oculai/scoring.py",
    "src/oculai/pipeline.py",
    "src/oculai/repositories.py",
    "src/oculai/postgres_repository.py",
    "src/oculai/sources/github.py",
    "src/oculai/sources/arxiv.py",
    "src/oculai/sources/dblp.py",
    "src/oculai/sources/scholarly.py",
    "src/oculai/sources/browser_profiles.py",
    "tests/test_pipeline.py",
    "web/index.html",
    "web/app.js",
    "web/styles.css",
]


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    missing = [path for path in REQUIRED_PATHS if not (root / path).exists()]
    if missing:
        print("Missing required Oculai project paths:")
        for path in missing:
            print(f"- {path}")
        return 1
    print("Oculai project structure looks complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
