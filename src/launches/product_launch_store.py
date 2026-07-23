"""JSON persistence for monitored product launches."""

from __future__ import annotations

import json
from pathlib import Path

from src.launches.product_launch import ProductLaunch


class ProductLaunchStore:
    def __init__(self, path: str | Path = "data/product_launches.json") -> None:
        self.path = Path(path)

    def load(self) -> list[ProductLaunch]:
        if not self.path.exists():
            return []
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return []
        if not isinstance(data, list):
            return []
        result = []
        for item in data:
            if isinstance(item, dict):
                try:
                    result.append(ProductLaunch.from_dict(item))
                except (TypeError, ValueError):
                    pass
        return result

    def save(self, launches: list[ProductLaunch]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.path.with_suffix(self.path.suffix + ".tmp")
        temporary.write_text(
            json.dumps([item.to_dict() for item in launches], indent=2, sort_keys=True),
            encoding="utf-8",
        )
        temporary.replace(self.path)
