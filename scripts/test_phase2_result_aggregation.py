"""Offline test for Phase 2 discovery result aggregation."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.discovery.discovery_result import SourceExecutionResult
from src.discovery.result_aggregator import ResultAggregator


def main() -> None:
    source_results = [
        SourceExecutionResult(
            source_name="Source A",
            elapsed_seconds=0.25,
            results=[
                {"title": "First", "link": "https://example.com/first"},
                {"title": "Shared", "link": "https://example.com/shared/"},
            ],
        ),
        SourceExecutionResult(
            source_name="Source B",
            elapsed_seconds=0.50,
            results=[
                {"title": "Duplicate", "url": "https://example.com/shared"},
                {"title": "Second", "link": "https://example.com/second"},
                {"title": "No link"},
            ],
        ),
        SourceExecutionResult(
            source_name="Broken Source",
            elapsed_seconds=0.10,
            error="offline test error",
        ),
    ]

    batch = ResultAggregator().aggregate(source_results)

    assert len(batch.results) == 4
    assert batch.duplicate_count == 1
    assert batch.source_count == 3
    assert batch.successful_source_count == 2
    assert batch.failed_source_count == 1
    assert abs(batch.total_elapsed_seconds - 0.85) < 0.000001
    assert batch.results[0]["source"] == "Source A"
    assert batch.results[2]["source"] == "Source B"

    print("Phase 2 result aggregation test passed.")


if __name__ == "__main__":
    main()
