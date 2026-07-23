import sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from src.workspaces.research_workspace_service import ResearchWorkspaceService
from src.workspaces.research_workspace_store import ResearchWorkspaceStore
from src.version import VERSION_INFO
def main():
 with tempfile.TemporaryDirectory() as d:
  store=ResearchWorkspaceStore(Path(d)/"workspaces.json");service=ResearchWorkspaceService(store)
  item=service.add("Camping Market Research","Australian camping products")
  service.update(item.workspace_id,status="Reviewing",questions="Which products are growing?",findings="Compact products show rising interest.",conclusions="Monitor spring launches.",linked_company_ids=["c1","c1"],linked_topic_ids=["t1"],linked_launch_ids=["l1"])
  saved=ResearchWorkspaceService(store).get(item.workspace_id)
  assert saved.status=="Reviewing" and saved.linked_company_ids==["c1"] and "rising" in saved.findings
  service.remove(item.workspace_id);assert service.workspaces==[]
 assert "ResearchWorkspaceService" in (ROOT/"src/ui/main_window.py").read_text()
 assert 'text="Workspaces"' in (ROOT/"src/ui/pipeline_window.py").read_text()
 ui=(ROOT/"src/ui/research_workspaces_window.py").read_text();assert "Add Workspace" in ui and "Save Workspace" in ui
 assert VERSION_INFO.package=="Package-023A-07" and VERSION_INFO.build==7
 print("Phase 5 research workspaces test passed.")
if __name__=="__main__":main()
