"""Create portable CSV pipeline exports and opportunity text reports."""

from __future__ import annotations

import csv
import re
from pathlib import Path


class ExportService:
    def __init__(
        self,
        pipeline_service,
        workflow_service,
        response_service,
        contact_service,
    ) -> None:
        self.pipeline_service = pipeline_service
        self.workflow_service = workflow_service
        self.response_service = response_service
        self.contact_service = contact_service

    def export_pipeline(
        self,
        path: str | Path,
        *,
        stage: str = "All",
        priority: str = "All",
    ) -> Path:
        destination = Path(path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        items = self.pipeline_service.items(stage=stage, priority=priority)
        with destination.open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(
                (
                    "Title",
                    "Status",
                    "Priority",
                    "Rating",
                    "Score",
                    "Follow-up Date",
                    "Checklist Progress",
                    "Draft Saved",
                    "Interactions",
                    "Source",
                    "URL",
                    "Notes",
                )
            )
            for item in items:
                record = item.record
                writer.writerow(
                    (
                        record.title,
                        record.status,
                        item.priority_label,
                        record.rating,
                        record.score,
                        record.follow_up_date,
                        f"{item.checklist_percent}%",
                        "Yes" if item.has_draft else "No",
                        item.interaction_count,
                        record.source,
                        record.url,
                        record.notes,
                    )
                )
        return destination

    def export_opportunity_report(
        self,
        record,
        path: str | Path,
    ) -> Path:
        destination = Path(path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(
            self.build_opportunity_report(record),
            encoding="utf-8",
        )
        return destination

    def build_opportunity_report(self, record) -> str:
        lines = [
            "OPPORTUNITYLAB OPPORTUNITY REPORT",
            "=" * 34,
            "",
            f"Title: {record.title}",
            f"Status: {record.status}",
            f"Rating: {record.rating}/5",
            f"Score: {record.score}/100",
            f"Source: {record.source}",
            f"URL: {record.url}",
            f"Follow-up date: {record.follow_up_date or 'Not set'}",
            "",
            "OPPORTUNITY NOTES",
            record.notes or "No notes saved.",
            "",
            "CONTACT",
        ]
        try:
            contact = self.contact_service.get_contact(record.tracking_id)
            lines.extend(
                (
                    f"Name: {contact.contact_name or 'Not set'}",
                    f"Organisation: {contact.organisation or 'Not set'}",
                    f"Email: {contact.email or 'Not set'}",
                    f"Phone: {contact.phone or 'Not set'}",
                    f"Website: {contact.website or 'Not set'}",
                    f"Notes: {contact.notes or 'None'}",
                )
            )
        except KeyError:
            lines.append("No contact saved.")

        lines.extend(("", "ACTION CHECKLIST"))
        try:
            workflow = self.workflow_service.get(record.tracking_id)
            lines.append(
                f"Progress: {workflow.completed_count}/{len(workflow.items)} "
                f"({workflow.progress_percent}%)"
            )
            for item in workflow.items:
                mark = "X" if item.completed else " "
                lines.append(f"[{mark}] {item.text}")
        except KeyError:
            lines.append("No checklist created.")

        lines.extend(("", "SAVED RESPONSE DRAFT"))
        draft = next(
            (
                item for item in self.response_service.drafts
                if item.tracking_id == record.tracking_id
            ),
            None,
        )
        if draft and (draft.subject or draft.body):
            lines.extend(
                (
                    f"Subject: {draft.subject}",
                    "",
                    draft.body,
                )
            )
        else:
            lines.append("No response draft saved.")

        lines.extend(("", "INTERACTION HISTORY"))
        history = self.contact_service.history(record.tracking_id)
        if history:
            for item in history:
                lines.append(
                    f"{item.interaction_date} | "
                    f"{item.interaction_type} | {item.summary}"
                )
        else:
            lines.append("No interaction history.")

        return "\n".join(lines).rstrip() + "\n"

    @staticmethod
    def suggested_report_name(title: str) -> str:
        safe_name = re.sub(r"[^A-Za-z0-9._-]+", "_", title).strip("._")
        return f"{safe_name or 'opportunity'}_report.txt"
