"""Computed pipeline view of a tracked opportunity."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PipelineItem:
    record: object
    priority_score: int
    priority_label: str
    checklist_percent: int
    has_draft: bool
    interaction_count: int
