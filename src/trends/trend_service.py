"""Manage market topics and summarise observations over time."""

from __future__ import annotations

from src.trends.market_topic import MarketTopic
from src.trends.trend_observation import TrendObservation
from src.trends.trend_store import TrendStore


class TrendService:
    DIRECTION_VALUE = {
        "Emerging": 2,
        "Rising": 2,
        "Stable": 0,
        "Falling": -2,
        "Volatile": 0,
    }

    def __init__(self, store: TrendStore | None = None) -> None:
        self.store = store or TrendStore()
        self.topics = self.store.load_topics()
        self.observations = self.store.load_observations()

    def add_topic(
        self,
        name: str,
        *,
        category: str = "Market",
        keywords=(),
        notes: str = "",
    ) -> MarketTopic:
        if isinstance(keywords, str):
            keywords = keywords.split(",")
        topic = MarketTopic(
            name=name,
            category=category,
            keywords=list(keywords),
            notes=str(notes).strip(),
        )
        self.topics.append(topic)
        self.store.save_topics(self.topics)
        return topic

    def get_topic(self, topic_id: str) -> MarketTopic:
        for topic in self.topics:
            if topic.topic_id == topic_id:
                return topic
        raise KeyError(topic_id)

    def add_observation(
        self,
        topic_id: str,
        *,
        direction: str,
        strength,
        summary: str,
        observation_date: str = "",
        source_title: str = "",
        source_url: str = "",
        notes: str = "",
    ) -> TrendObservation:
        self.get_topic(topic_id)
        item = TrendObservation(
            topic_id=topic_id,
            direction=direction,
            strength=int(strength),
            summary=summary,
            **(
                {"observation_date": observation_date}
                if observation_date else {}
            ),
            source_title=str(source_title).strip(),
            source_url=str(source_url).strip(),
            notes=str(notes).strip(),
        )
        self.observations.append(item)
        self.store.save_observations(self.observations)
        return item

    def for_topic(self, topic_id: str) -> list[TrendObservation]:
        return sorted(
            (
                item for item in self.observations
                if item.topic_id == topic_id
            ),
            key=lambda item: (item.observation_date, item.created_at),
            reverse=True,
        )

    def summary(self, topic_id: str) -> dict[str, object]:
        items = self.for_topic(topic_id)
        if not items:
            return {
                "observations": 0,
                "latest_direction": "No data",
                "average_strength": 0.0,
                "momentum": 0,
                "sourced": 0,
            }
        weighted_values = [
            self.DIRECTION_VALUE[item.direction] * item.strength
            for item in items
        ]
        return {
            "observations": len(items),
            "latest_direction": items[0].direction,
            "average_strength": round(
                sum(item.strength for item in items) / len(items),
                1,
            ),
            "momentum": round(sum(weighted_values) / len(items), 1),
            "sourced": sum(bool(item.source_url) for item in items),
        }

    def remove_observation(self, observation_id: str) -> None:
        original_count = len(self.observations)
        self.observations = [
            item for item in self.observations
            if item.observation_id != observation_id
        ]
        if len(self.observations) == original_count:
            raise KeyError(observation_id)
        self.store.save_observations(self.observations)

    def remove_topic(self, topic_id: str) -> None:
        self.get_topic(topic_id)
        self.topics = [
            topic for topic in self.topics
            if topic.topic_id != topic_id
        ]
        self.observations = [
            item for item in self.observations
            if item.topic_id != topic_id
        ]
        self.store.save_topics(self.topics)
        self.store.save_observations(self.observations)
