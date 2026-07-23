"""JSON persistence for company intelligence profiles."""

from __future__ import annotations

import json
from pathlib import Path

from src.companies.company_profile import CompanyProfile


class CompanyProfileStore:
    def __init__(
        self,
        path: str | Path = "data/company_profiles.json",
    ) -> None:
        self.path = Path(path)

    def load(self) -> list[CompanyProfile]:
        if not self.path.exists():
            return []
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return []
        if not isinstance(data, list):
            return []
        profiles = []
        for item in data:
            if not isinstance(item, dict):
                continue
            try:
                profiles.append(CompanyProfile.from_dict(item))
            except (TypeError, ValueError):
                continue
        return profiles

    def save(self, profiles: list[CompanyProfile]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.path.with_suffix(self.path.suffix + ".tmp")
        temporary.write_text(
            json.dumps(
                [profile.to_dict() for profile in profiles],
                indent=2,
                sort_keys=True,
            ),
            encoding="utf-8",
        )
        temporary.replace(self.path)
