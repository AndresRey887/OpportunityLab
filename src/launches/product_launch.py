"""A product launch monitored by OpportunityLab."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from uuid import uuid4


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class ProductLaunch:
    product_name: str
    company_id: str = ""
    company_name: str = ""
    stage: str = "Announced"
    launch_date: str = ""
    category: str = ""
    source_url: str = ""
    notes: str = ""
    alert_days: int = 14
    launch_id: str = field(default_factory=lambda: uuid4().hex)
    updated_at: str = field(default_factory=utc_now)

    STAGES = (
        "Rumoured",
        "Announced",
        "Pre-launch",
        "Released",
        "Delayed",
        "Cancelled",
    )

    def __post_init__(self) -> None:
        self.product_name = str(self.product_name).strip()
        if not self.product_name:
            raise ValueError("Product name cannot be empty.")
        if self.stage not in self.STAGES:
            self.stage = "Announced"
        self.alert_days = max(0, min(int(self.alert_days or 0), 365))

    def touch(self) -> None:
        self.updated_at = utc_now()

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "ProductLaunch":
        return cls(
            product_name=str(data.get("product_name", "")),
            company_id=str(data.get("company_id", "")),
            company_name=str(data.get("company_name", "")),
            stage=str(data.get("stage", "Announced")),
            launch_date=str(data.get("launch_date", "")),
            category=str(data.get("category", "")),
            source_url=str(data.get("source_url", "")),
            notes=str(data.get("notes", "")),
            alert_days=int(data.get("alert_days", 14) or 0),
            launch_id=str(data.get("launch_id") or uuid4().hex),
            updated_at=str(data.get("updated_at") or utc_now()),
        )
