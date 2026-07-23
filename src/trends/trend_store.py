"""JSON persistence for market topics and trend observations."""

from __future__ import annotations

import json
from pathlib import Path

from src.trends.market_topic import MarketTopic
from src.trends.trend_observation import TrendObservation


class TrendStore:
    def __init__(
        self,
        topic_path: str | Path = "data/market_topics.json",
        observation_path: str | Path = "data/trend_observations.json",
    ) -> None:
        self.topic_path = Path(topic_path)
        self.observation_path = Path(observation_path)

    def load_topics(self) -> list[MarketTopic]:
        return self._load(self.topic_path, MarketTopic.from_dict)

    def load_observations(self) -> list[TrendObservation]:
        return self._load(
            self.observation_path,
            TrendObservation.from_dict,
        )

    def save_topics(self, topics: list[MarketTopic]) -> None:
        self._save(self.topic_path, [topic.to_dict() for topic in topics])

    def save_observations(
        self,
        observations: list[TrendObservation],
    ) -> None:
        self._save(
            self.observation_path,
            [item.to_dict() for item in observations],
        )

    @staticmethod
    def _load(path: Path, factory) -> list:
        if not path.exists():
            return []
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return []
        if not isinstance(data, list):
            return []
        result = []
        for item in data:
            if not isinstance(item, dict):
                continue
            try:
                result.append(factory(item))
            except (TypeError, ValueError):
                continue
        return result

    @staticmethod
    def _save(path: Path, data: list[dict]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_suffix(path.suffix + ".tmp")
        temporary.write_text(
            json.dumps(data, indent=2, sort_keys=True),
            encoding="utf-8",
        )
        temporary.replace(path)
