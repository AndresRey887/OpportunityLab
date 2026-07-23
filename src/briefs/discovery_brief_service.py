from pathlib import Path

class DiscoveryBriefService:
    def __init__(self, companies, evidence, competitors, trends, signals, launches):
        self.companies=companies; self.evidence=evidence; self.competitors=competitors
        self.trends=trends; self.signals=signals; self.launches=launches
    def export(self, workspace, path):
        destination=Path(path); destination.parent.mkdir(parents=True,exist_ok=True)
        destination.write_text(self.build(workspace),encoding="utf-8"); return destination
    def build(self, workspace):
        lines=["OPPORTUNITYLAB DISCOVERY RESEARCH BRIEF","="*40,"",f"Workspace: {workspace.title}",f"Status: {workspace.status}",f"Focus: {workspace.focus or 'Not set'}","", "RESEARCH QUESTIONS",workspace.questions or "None recorded.","","FINDINGS",workspace.findings or "None recorded.","","CONCLUSIONS AND NEXT ACTIONS",workspace.conclusions or "None recorded.","","LINKED COMPANIES"]
        profiles=[p for p in self.companies.profiles if p.company_id in workspace.linked_company_ids]
        if not profiles: lines.append("No companies linked.")
        for p in profiles:
            s=self.evidence.summary(p.company_id)
            lines.extend([f"- {p.name} | {p.industry or 'Industry not set'} | {p.location or 'Location not set'}",f"  Evidence: {s['total']} ({s['high_confidence']} high confidence) | Competitors: {len(self.competitors.for_company(p.company_id))}"])
        lines.extend(["","LINKED MARKET TOPICS"])
        topics=[t for t in self.trends.topics if t.topic_id in workspace.linked_topic_ids]
        if not topics: lines.append("No market topics linked.")
        for t in topics:
            s=self.trends.summary(t.topic_id); lines.append(f"- {t.name} | {s['latest_direction']} | Momentum {s['momentum']} | {s['observations']} observations")
        lines.extend(["","LINKED PRODUCT LAUNCHES"])
        launches=[l for l in self.launches.launches if l.launch_id in workspace.linked_launch_ids]
        if not launches: lines.append("No product launches linked.")
        for l in launches: lines.append(f"- {l.product_name} | {l.company_name or 'No company'} | {l.stage} | {l.launch_date or 'No date'}")
        signal_summary=self.signals.summary()
        lines.extend(["","SOCIAL SIGNAL SUMMARY",f"Signals: {signal_summary['total']} | Positive: {signal_summary['positive']} | Negative: {signal_summary['negative']} | Average strength: {signal_summary['average_strength']}/5","", "Generated from saved OpportunityLab intelligence."])
        return "\n".join(lines).rstrip()+"\n"
