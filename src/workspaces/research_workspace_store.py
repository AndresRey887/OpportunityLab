import json
from pathlib import Path
from src.workspaces.research_workspace import ResearchWorkspace

class ResearchWorkspaceStore:
    def __init__(self, path="data/research_workspaces.json"):
        self.path = Path(path)
    def load(self):
        if not self.path.exists():
            return []
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
            return [ResearchWorkspace.from_dict(item) for item in data if isinstance(item, dict)]
        except (OSError, ValueError, TypeError, json.JSONDecodeError):
            return []
    def save(self, items):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.path.with_suffix(self.path.suffix + ".tmp")
        temporary.write_text(json.dumps([item.to_dict() for item in items], indent=2, sort_keys=True), encoding="utf-8")
        temporary.replace(self.path)
