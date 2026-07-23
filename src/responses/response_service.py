"""Manage reusable response templates and saved opportunity drafts."""

from __future__ import annotations

from src.responses.opportunity_draft import OpportunityDraft
from src.responses.response_store import ResponseStore
from src.responses.response_template import ResponseTemplate


class ResponseService:
    DEFAULT_TEMPLATES = (
        (
            "General Enquiry",
            "Enquiry about {title}",
            "Hello,\n\nI am interested in {title}. Could you please provide "
            "more information about the opportunity, eligibility, and next "
            "steps?\n\nOpportunity link: {url}\n\nKind regards,",
        ),
        (
            "Expression of Interest",
            "Expression of interest — {title}",
            "Hello,\n\nI would like to register my interest in {title}. "
            "Please let me know what information you require and any important "
            "deadlines.\n\nI found this through {source}.\n\nKind regards,",
        ),
        (
            "Follow-up",
            "Following up — {title}",
            "Hello,\n\nI am following up regarding {title}. Could you please "
            "let me know whether there are any updates or actions required "
            "from me?\n\nKind regards,",
        ),
    )

    def __init__(
        self,
        store: ResponseStore | None = None,
        timeline_service=None,
    ) -> None:
        self.store = store or ResponseStore()
        self.timeline_service = timeline_service
        self.templates = self.store.load_templates()
        self.drafts = self.store.load_drafts()
        if not self.templates:
            self.templates = [
                ResponseTemplate(
                    name=name,
                    subject=subject,
                    body=body,
                    built_in=True,
                )
                for name, subject, body in self.DEFAULT_TEMPLATES
            ]
            self.store.save_templates(self.templates)

    def template_names(self) -> list[str]:
        return [template.name for template in self.templates]

    def get_template_by_name(self, name: str) -> ResponseTemplate:
        for template in self.templates:
            if template.name == name:
                return template
        raise KeyError(name)

    def add_template(self, name: str, subject: str, body: str) -> ResponseTemplate:
        template = ResponseTemplate(name=name, subject=subject, body=body)
        self.templates.append(template)
        self.store.save_templates(self.templates)
        return template

    def get_or_create_draft(self, record) -> OpportunityDraft:
        for draft in self.drafts:
            if draft.tracking_id == record.tracking_id:
                return draft
        draft = OpportunityDraft(
            tracking_id=record.tracking_id,
            title=record.title,
        )
        self.drafts.append(draft)
        self.store.save_drafts(self.drafts)
        return draft

    def apply_template(
        self,
        draft: OpportunityDraft,
        template: ResponseTemplate,
        record,
    ) -> OpportunityDraft:
        values = {
            "title": record.title,
            "url": record.url,
            "source": record.source or "OpportunityLab",
        }
        draft.template_id = template.template_id
        draft.subject = self._render(template.subject, values)
        draft.body = self._render(template.body, values)
        draft.touch()
        self.store.save_drafts(self.drafts)
        self._record(
            draft.tracking_id,
            "Response template applied",
            template.name,
        )
        return draft

    def save_draft(
        self,
        tracking_id: str,
        *,
        subject: str,
        body: str,
    ) -> OpportunityDraft:
        for draft in self.drafts:
            if draft.tracking_id == tracking_id:
                draft.subject = str(subject).strip()
                draft.body = str(body).strip()
                draft.touch()
                self.store.save_drafts(self.drafts)
                self._record(
                    tracking_id,
                    "Response draft saved",
                    draft.subject,
                )
                return draft
        raise KeyError(tracking_id)

    @staticmethod
    def _render(text: str, values: dict[str, str]) -> str:
        rendered = text
        for name, value in values.items():
            rendered = rendered.replace("{" + name + "}", value)
        return rendered

    def _record(self, tracking_id, title, details=""):
        if self.timeline_service is not None:
            self.timeline_service.record(
                tracking_id,
                "Draft",
                title,
                details,
            )
