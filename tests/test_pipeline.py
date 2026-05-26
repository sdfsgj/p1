import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from oculai.jd_parser import DeterministicJDParser
from oculai.pipeline import TalentPipeline
from oculai.repositories import JsonCandidateRepository
from oculai.sources.arxiv import ArxivSource
from oculai.sources.dblp import DblpSource
from oculai.sources.github import GitHubSource
from oculai.sources.scholarly import OpenAlexSource, SemanticScholarSource


class PipelineTests(unittest.TestCase):
    def test_parse_job_description_extracts_core_signals(self):
        profile = DeterministicJDParser().parse(
            "Senior AI engineer with 8+ years, Python, LLM, RAG, PostgreSQL, English, US."
        )

        self.assertIn("Python", profile.skills)
        self.assertIn("LLM", profile.skills)
        self.assertIn("RAG", profile.skills)
        self.assertIn("PostgreSQL", profile.skills)
        self.assertIn("English", profile.languages)
        self.assertEqual(profile.minimum_years, 8)

    def test_analyze_returns_ranked_candidates(self):
        pipeline = TalentPipeline(JsonCandidateRepository(ROOT / "data" / "candidates.json"))
        result = pipeline.analyze(
            "Need a staff LLM RAG Python PostgreSQL engineer with research experience.",
            limit=3,
        )

        candidates = result["candidates"]
        self.assertEqual(len(candidates), 3)
        scores = [candidate["score"] for candidate in candidates]
        self.assertEqual(scores, sorted(scores, reverse=True))
        self.assertGreaterEqual(candidates[0]["score"], 60)

    def test_source_adapters_build_expected_api_urls(self):
        profile = DeterministicJDParser().parse("LLM RAG Python Semantic Scholar OpenAlex engineer")

        self.assertIn("api.github.com", GitHubSource().build_search_url(profile, limit=5))
        self.assertIn("semanticscholar.org", SemanticScholarSource().build_search_url(profile, limit=5))
        self.assertIn("api.openalex.org", OpenAlexSource().build_search_url(profile, limit=5))
        self.assertIn("export.arxiv.org", ArxivSource().build_search_url(profile, limit=5))
        self.assertIn("dblp.org", DblpSource().build_search_url(profile, limit=5))


if __name__ == "__main__":
    unittest.main()
