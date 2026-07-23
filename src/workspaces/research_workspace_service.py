from src.workspaces.research_workspace import ResearchWorkspace, now
from src.workspaces.research_workspace_store import ResearchWorkspaceStore

class ResearchWorkspaceService:
    def __init__(self, store=None):
        self.store = store or ResearchWorkspaceStore()
        self.workspaces = self.store.load()
    def add(self, title, focus=""):
        item = ResearchWorkspace(title=title, focus=focus)
        self.workspaces.append(item)
        self.store.save(self.workspaces)
        return item
    def get(self, workspace_id):
        for item in self.workspaces:
            if item.workspace_id == workspace_id:
                return item
        raise KeyError(workspace_id)
    def update(self, workspace_id, **values):
        item = self.get(workspace_id)
        for name in ("title", "focus", "status", "questions", "findings", "conclusions"):
            if name in values:
                setattr(item, name, str(values[name]).strip())
        if item.status not in ResearchWorkspace.STATUSES:
            raise ValueError(item.status)
        for name in ("linked_company_ids", "linked_topic_ids", "linked_launch_ids"):
            if name in values:
                setattr(item, name, list(dict.fromkeys(values[name])))
        item.updated_at = now()
        self.store.save(self.workspaces)
        return item
    def remove(self, workspace_id):
        self.get(workspace_id)
        self.workspaces = [item for item in self.workspaces if item.workspace_id != workspace_id]
        self.store.save(self.workspaces)
