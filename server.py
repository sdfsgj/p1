from __future__ import annotations

import json
import os
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

ROOT = Path(__file__).parent
SRC_ROOT = ROOT / "src"
WEB_ROOT = ROOT / "web"
DATA_PATH = ROOT / "data" / "candidates.json"

sys.path.insert(0, str(SRC_ROOT))

from oculai.pipeline import TalentPipeline  # noqa: E402
from oculai.repositories import JsonCandidateRepository  # noqa: E402


def build_pipeline() -> TalentPipeline:
    return TalentPipeline(repository=JsonCandidateRepository(DATA_PATH))


class OculaiHandler(SimpleHTTPRequestHandler):
    pipeline = build_pipeline()

    def translate_path(self, path: str) -> str:
        parsed = urlparse(path)
        if parsed.path == "/":
            return str(WEB_ROOT / "index.html")
        if parsed.path.startswith("/web/"):
            return str(ROOT / parsed.path.lstrip("/"))
        return str(WEB_ROOT / parsed.path.lstrip("/"))

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/api/health":
            self.write_json({"ok": True, "service": "oculai", "mode": "local"})
            return
        if parsed.path == "/api/candidates":
            candidates = [candidate.to_dict() for candidate in self.pipeline.repository.list_candidates()]
            self.write_json({"candidates": candidates})
            return
        super().do_GET()

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path != "/api/analyze":
            self.send_error(404)
            return
        length = int(self.headers.get("Content-Length", "0"))
        payload = json.loads(self.rfile.read(length) or b"{}")
        jd = str(payload.get("job_description", "")).strip()
        limit = int(payload.get("limit", 10))
        if not jd:
            self.write_json({"error": "job_description is required"}, status=400)
            return
        self.write_json(self.pipeline.analyze(jd, limit=limit))

    def write_json(self, payload: dict[str, Any], status: int = 200) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main() -> None:
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    server = ThreadingHTTPServer((host, port), OculaiHandler)
    print(f"Oculai running at http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
