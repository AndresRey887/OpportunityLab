"""Cluster likely duplicate discoveries while preserving every source."""

from __future__ import annotations

import re
from difflib import SequenceMatcher
from hashlib import sha256
from urllib.parse import urlparse

from src.clustering.duplicate_cluster import DuplicateCluster, DuplicateMatch
from src.clustering.duplicate_decision_store import DuplicateDecisionStore


class DuplicateClusterService:
    STOP_WORDS = {
        "a", "an", "and", "apply", "for", "in", "join", "of", "on",
        "opportunity", "program", "the", "to", "with",
    }

    def __init__(
        self,
        decision_store: DuplicateDecisionStore | None = None,
    ) -> None:
        self.decision_store = decision_store or DuplicateDecisionStore()
        self.ignored_pairs = self.decision_store.load_ignored()

    def find_clusters(self, records: list | tuple) -> list[DuplicateCluster]:
        ordered = sorted(
            records,
            key=lambda record: (record.rating, record.score, record.updated_at),
            reverse=True,
        )
        used = set()
        clusters = []
        for primary in ordered:
            if primary.tracking_id in used:
                continue
            matches = []
            for candidate in ordered:
                if (
                    candidate.tracking_id == primary.tracking_id
                    or candidate.tracking_id in used
                    or self.is_ignored(primary, candidate)
                ):
                    continue
                match = self.compare(primary, candidate)
                if match is not None:
                    matches.append(match)
            if matches:
                matches.sort(key=lambda match: match.confidence, reverse=True)
                clusters.append(
                    DuplicateCluster(
                        primary=primary,
                        matches=tuple(matches),
                    )
                )
                used.add(primary.tracking_id)
                used.update(match.record.tracking_id for match in matches)
        return sorted(
            clusters,
            key=lambda cluster: (
                cluster.highest_confidence,
                cluster.member_count,
            ),
            reverse=True,
        )

    def compare(self, first, second) -> DuplicateMatch | None:
        first_title = self._normalise_title(first.title)
        second_title = self._normalise_title(second.title)
        if not first_title or not second_title:
            return None

        sequence = SequenceMatcher(None, first_title, second_title).ratio()
        first_tokens = set(first_title.split())
        second_tokens = set(second_title.split())
        union = first_tokens | second_tokens
        token_similarity = (
            len(first_tokens & second_tokens) / len(union)
            if union else 0.0
        )
        first_domain = self._domain(first.url)
        second_domain = self._domain(second.url)
        same_domain = bool(first_domain and first_domain == second_domain)

        raw_confidence = max(sequence, token_similarity)
        if same_domain:
            raw_confidence = min(1.0, raw_confidence + 0.15)

        threshold = 0.58 if same_domain else 0.72
        if raw_confidence < threshold:
            return None

        reasons = []
        if token_similarity >= 0.55:
            reasons.append("similar title words")
        elif sequence >= 0.65:
            reasons.append("similar title")
        if same_domain:
            reasons.append("same website")
        if getattr(first, "source", "") != getattr(second, "source", ""):
            reasons.append("multiple sources")

        return DuplicateMatch(
            record=second,
            confidence=round(raw_confidence * 100),
            reasons=tuple(reasons or ("possible duplicate",)),
        )

    def ignore_pair(self, first, second) -> None:
        self.ignored_pairs.add(self._pair_key(first, second))
        self.decision_store.save_ignored(self.ignored_pairs)

    def is_ignored(self, first, second) -> bool:
        return self._pair_key(first, second) in self.ignored_pairs

    @classmethod
    def _normalise_title(cls, title: str) -> str:
        words = re.findall(r"[a-z0-9]+", str(title).casefold())
        return " ".join(word for word in words if word not in cls.STOP_WORDS)

    @staticmethod
    def _domain(url: str) -> str:
        domain = (urlparse(str(url)).hostname or "").casefold()
        return domain[4:] if domain.startswith("www.") else domain

    @staticmethod
    def _pair_key(first, second) -> str:
        values = sorted((first.tracking_id, second.tracking_id))
        return sha256("|".join(values).encode("utf-8")).hexdigest()
