"""Export a portable snapshot of Pathfinder learning and decision data."""

from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

from src.version import VERSION_INFO


class LearningExportService:
    def __init__(
        self,
        review_service,
        memory_service,
        outcome_service,
        feedback_service,
        duplicate_cluster_service,
    ) -> None:
        self.review = review_service
        self.memory = memory_service
        self.outcomes = outcome_service
        self.feedback = feedback_service
        self.clusters = duplicate_cluster_service

    def export(self, path: str | Path) -> Path:
        destination = Path(path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(
            json.dumps(
                self.build_snapshot(),
                indent=2,
                sort_keys=True,
            ),
            encoding="utf-8",
        )
        return destination

    def build_snapshot(self) -> dict:
        tracked = self.memory.tracking_service.records
        clusters = self.clusters.find_clusters(tracked)
        return {
            "application": VERSION_INFO.app_name,
            "version": VERSION_INFO.version,
            "package": VERSION_INFO.package,
            "exported_at": datetime.now(timezone.utc).isoformat(),
            "decision_summary": self.review.summary(),
            "outcome_totals": self.review.outcome_totals(),
            "strong_patterns": [
                asdict(pattern)
                for pattern in self.review.strong_patterns(limit=50)
            ],
            "weak_patterns": [
                asdict(pattern)
                for pattern in self.review.weak_patterns(limit=50)
            ],
            "evidence_gaps": self.review.evidence_gaps(),
            "lessons": self.review.lessons(limit=50),
            "source_profiles": [
                asdict(profile)
                for profile in self.memory.source_profiles()
            ],
            "keyword_profiles": [
                asdict(profile)
                for profile in self.memory.keyword_profiles(limit=100)
            ],
            "opportunity_type_profiles": [
                asdict(profile)
                for profile in self.memory.opportunity_type_profiles()
            ],
            "outcomes": [
                outcome.to_dict()
                for outcome in self.outcomes.records
            ],
            "recommendation_feedback": [
                item.to_dict()
                for item in self.feedback.feedback
            ],
            "duplicate_families": [
                {
                    "primary_tracking_id": cluster.primary.tracking_id,
                    "primary_title": cluster.primary.title,
                    "member_count": cluster.member_count,
                    "highest_confidence": cluster.highest_confidence,
                    "matches": [
                        {
                            "tracking_id": match.record.tracking_id,
                            "title": match.record.title,
                            "confidence": match.confidence,
                            "reasons": list(match.reasons),
                        }
                        for match in cluster.matches
                    ],
                }
                for cluster in clusters
            ],
        }
