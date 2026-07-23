from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from uuid import uuid4

def now():
    return datetime.now(timezone.utc).isoformat()

@dataclass
class ResearchWorkspace:
    title: str
    focus: str = ""
    status: str = "Researching"
    questions: str = ""
    findings: str = ""
    conclusions: str = ""
    linked_company_ids: list[str] = field(default_factory=list)
    linked_topic_ids: list[str] = field(default_factory=list)
    linked_launch_ids: list[str] = field(default_factory=list)
    workspace_id: str = field(default_factory=lambda: uuid4().hex)
    updated_at: str = field(default_factory=now)
    STATUSES = ("Planning", "Researching", "Reviewing", "Complete", "Archived")

    def __post_init__(self):
        self.title = str(self.title).strip()
        if not self.title:
            raise ValueError("Workspace title is required.")
        if self.status not in self.STATUSES:
            self.status = "Researching"

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        allowed = cls.__dataclass_fields__
        return cls(**{key: value for key, value in data.items() if key in allowed})
