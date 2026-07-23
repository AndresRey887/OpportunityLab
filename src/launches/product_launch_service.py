"""Manage product launches and upcoming date alerts."""

from __future__ import annotations

from collections import Counter
from datetime import date, timedelta

from src.launches.product_launch import ProductLaunch
from src.launches.product_launch_store import ProductLaunchStore


class ProductLaunchService:
    def __init__(self, store: ProductLaunchStore | None = None) -> None:
        self.store = store or ProductLaunchStore()
        self.launches = self.store.load()

    def add(self, **values) -> ProductLaunch:
        item = ProductLaunch(**values)
        self.launches.append(item)
        self.store.save(self.launches)
        return item

    def all(self, stage: str = "All") -> list[ProductLaunch]:
        items = self.launches
        if stage != "All":
            items = [item for item in items if item.stage == stage]
        return sorted(items, key=lambda item: (item.launch_date or "9999", item.product_name))

    def upcoming(self, days: int = 30, today: date | None = None) -> list[ProductLaunch]:
        today = today or date.today()
        limit = today + timedelta(days=max(0, days))
        return [
            item for item in self.all()
            if item.stage not in {"Released", "Cancelled"}
            and self._date(item.launch_date) is not None
            and today <= self._date(item.launch_date) <= limit
        ]

    def overdue(self, today: date | None = None) -> list[ProductLaunch]:
        today = today or date.today()
        return [
            item for item in self.all()
            if item.stage not in {"Released", "Cancelled", "Delayed"}
            and self._date(item.launch_date) is not None
            and self._date(item.launch_date) < today
        ]

    def update_stage(self, launch_id: str, stage: str) -> ProductLaunch:
        item = self.get(launch_id)
        if stage not in ProductLaunch.STAGES:
            raise ValueError(stage)
        item.stage = stage
        item.touch()
        self.store.save(self.launches)
        return item

    def get(self, launch_id: str) -> ProductLaunch:
        for item in self.launches:
            if item.launch_id == launch_id:
                return item
        raise KeyError(launch_id)

    def summary(self, today: date | None = None) -> dict[str, object]:
        stages = Counter(item.stage for item in self.launches)
        return {
            "total": len(self.launches),
            "upcoming_30": len(self.upcoming(30, today)),
            "overdue": len(self.overdue(today)),
            "released": stages.get("Released", 0),
            "stages": dict(stages),
        }

    def remove(self, launch_id: str) -> None:
        self.get(launch_id)
        self.launches = [item for item in self.launches if item.launch_id != launch_id]
        self.store.save(self.launches)

    @staticmethod
    def _date(value: str) -> date | None:
        try:
            return date.fromisoformat(value)
        except (TypeError, ValueError):
            return None
