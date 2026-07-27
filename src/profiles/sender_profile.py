"""A personal or organisation identity used across OpportunityLab."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from uuid import uuid4


@dataclass
class SenderProfile:
    name: str
    sender_name: str = ""
    role: str = ""
    organisation: str = ""
    email: str = ""
    website: str = ""
    address: str = ""
    organisation_description: str = ""
    charity_information: str = ""
    signature: str = ""
    tone: str = "Professional"
    profile_type: str = "Personal"
    mission: str = ""
    beneficiaries: str = ""
    service_area: str = ""
    support_needs: str = ""
    opportunity_types: str = ""
    dgr_status: str = ""
    profile_id: str = field(default_factory=lambda: uuid4().hex)

    @property
    def is_nonprofit(self) -> bool:
        value = self.profile_type.casefold().replace("-", "").replace(" ", "")
        return value in {"nonprofit", "charity", "notforprofit"}

    def to_dict(self) -> dict[str, str]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "SenderProfile":
        values = {
            name: data.get(name, field_info.default)
            for name, field_info in cls.__dataclass_fields__.items()
            if name != "profile_id"
        }
        values["profile_id"] = str(data.get("profile_id") or uuid4().hex)
        return cls(**values)
