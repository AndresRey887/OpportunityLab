"""Offline test for Phase 4 duplicate opportunity clustering."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.clustering.duplicate_cluster_service import DuplicateClusterService
from src.clustering.duplicate_decision_store import DuplicateDecisionStore
from src.models.opportunity import Opportunity
from src.tracking.tracking_service import TrackingService
from src.tracking.tracking_store import TrackingStore
from src.version import VERSION_INFO


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        tracking = TrackingService(TrackingStore(root / "tracked.json"))
        primary, _ = tracking.track(
            Opportunity(
                title="Acme Product Testing Program Australia",
                url="https://acme.example.com/testing/apply",
                source="Company Websites",
                score=91,
            )
        )
        related, _ = tracking.track(
            Opportunity(
                title="Join Acme Australian Product Testing Program",
                url="https://acme.example.com/news/product-testing",
                source="Serper",
                score=84,
            )
        )
        unrelated, _ = tracking.track(
            Opportunity(
                title="Regional Woodworking Grant",
                url="https://grants.example.org/woodworking",
                source="Serper",
                score=77,
            )
        )
        tracking.update(primary.tracking_id, rating=5)

        decision_store = DuplicateDecisionStore(root / "decisions.json")
        service = DuplicateClusterService(decision_store)
        clusters = service.find_clusters(tracking.records)
        assert len(clusters) == 1
        cluster = clusters[0]
        assert cluster.primary.tracking_id == primary.tracking_id
        assert cluster.member_count == 2
        assert cluster.matches[0].record.tracking_id == related.tracking_id
        assert cluster.matches[0].confidence >= 70
        assert "same website" in cluster.matches[0].reasons
        assert "multiple sources" in cluster.matches[0].reasons
        assert all(
            match.record.tracking_id != unrelated.tracking_id
            for match in cluster.matches
        )

        service.ignore_pair(primary, related)
        assert service.find_clusters(tracking.records) == []
        reloaded = DuplicateClusterService(decision_store)
        assert reloaded.is_ignored(primary, related)
        assert reloaded.find_clusters(tracking.records) == []

    main_window = (PROJECT_ROOT / "src/ui/main_window.py").read_text(
        encoding="utf-8"
    )
    pipeline_window = (PROJECT_ROOT / "src/ui/pipeline_window.py").read_text(
        encoding="utf-8"
    )
    clusters_window = (
        PROJECT_ROOT / "src/ui/duplicate_clusters_window.py"
    ).read_text(encoding="utf-8")
    assert "DuplicateClusterService" in main_window
    assert 'text="Clusters"' in pipeline_window
    assert "Related Opportunity Families" in clusters_window
    assert "Not Related" in clusters_window
    assert VERSION_INFO.package == "Package-022A-03"
    assert VERSION_INFO.build == 3

    print("Phase 4 duplicate clustering test passed.")


if __name__ == "__main__":
    main()
