from __future__ import annotations

from .jd_parser import DeterministicJDParser
from .models import CandidateEvaluation, PhaseStatus, PipelinePhase
from .repositories import CandidateRepository
from .scoring import CandidateScorer


class TalentPipeline:
    def __init__(
        self,
        repository: CandidateRepository,
        parser: DeterministicJDParser | None = None,
        scorer: CandidateScorer | None = None,
    ) -> None:
        self.repository = repository
        self.parser = parser or DeterministicJDParser()
        self.scorer = scorer or CandidateScorer()

    def analyze(self, job_description: str, limit: int = 10) -> dict[str, object]:
        profile = self.parser.parse(job_description)
        candidates = self.repository.list_candidates()
        ranked = sorted(
            [self.scorer.score(profile, candidate) for candidate in candidates],
            key=lambda evaluation: evaluation.score,
            reverse=True,
        )[:limit]

        return {
            "profile": profile.to_dict(),
            "pipeline": [phase.to_dict() for phase in self.phases()],
            "candidates": [evaluation.to_dict() for evaluation in ranked],
        }

    @staticmethod
    def phases() -> list[PipelinePhase]:
        return [
            PipelinePhase("Phase 0", "Requirement parsing", PhaseStatus.COMPLETE),
            PipelinePhase("Phase 1", "Wide search", PhaseStatus.COMPLETE),
            PipelinePhase("Phase 2", "Semantic matching", PhaseStatus.COMPLETE),
            PipelinePhase("Phase 3", "Deep research", PhaseStatus.SIMULATED),
            PipelinePhase("Phase 4", "Evaluation scoring", PhaseStatus.COMPLETE),
            PipelinePhase("Phase 5", "Outreach strategy", PhaseStatus.COMPLETE),
            PipelinePhase("Phase 6", "Closed-loop tracking", PhaseStatus.READY),
        ]

