import sys,tempfile
from pathlib import Path
from types import SimpleNamespace
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from src.briefs.discovery_brief_service import DiscoveryBriefService
from src.version import VERSION_INFO
def main():
 company=SimpleNamespace(company_id="c1",name="Acme",industry="Outdoor",location="Victoria")
 companies=SimpleNamespace(profiles=[company])
 evidence=SimpleNamespace(summary=lambda company_id:{"total":2,"high_confidence":1})
 competitors=SimpleNamespace(for_company=lambda company_id:[object()])
 topic=SimpleNamespace(topic_id="t1",name="Camping Demand")
 trends=SimpleNamespace(topics=[topic],summary=lambda topic_id:{"latest_direction":"Rising","momentum":8,"observations":3})
 launch=SimpleNamespace(launch_id="l1",product_name="Camp Stove",company_name="Acme",stage="Pre-launch",launch_date="2026-09-01")
 launches=SimpleNamespace(launches=[launch])
 signals=SimpleNamespace(summary=lambda:{"total":4,"positive":3,"negative":1,"average_strength":4.0})
 workspace=SimpleNamespace(title="Outdoor Research",status="Reviewing",focus="Camping products",questions="What is growing?",findings="Demand is rising.",conclusions="Monitor launches.",linked_company_ids=["c1"],linked_topic_ids=["t1"],linked_launch_ids=["l1"])
 service=DiscoveryBriefService(companies,evidence,competitors,trends,signals,launches)
 brief=service.build(workspace)
 for text in ("Acme","Camping Demand","Camp Stove","Signals: 4","Demand is rising."):assert text in brief
 with tempfile.TemporaryDirectory() as d: assert service.export(workspace,Path(d)/"brief.txt").read_text()==brief
 assert "DiscoveryBriefService" in (ROOT/"src/ui/main_window.py").read_text()
 assert "Export Brief" in (ROOT/"src/ui/research_workspaces_window.py").read_text()
 assert VERSION_INFO.package=="Package-023A-08" and VERSION_INFO.build==8
 print("Phase 5 complete test passed.")
if __name__=="__main__":main()
