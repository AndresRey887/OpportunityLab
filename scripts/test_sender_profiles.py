"""Verify sender profiles and profile-aware response drafts."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.profiles.sender_profile_service import SenderProfileService
from src.responses.response_service import ResponseService
from src.version import VERSION_INFO


class MemoryStore:
    def __init__(self):
        self.templates = []
        self.drafts = []

    def load_templates(self):
        return self.templates

    def save_templates(self, templates):
        self.templates = templates

    def load_drafts(self):
        return self.drafts

    def save_drafts(self, drafts):
        self.drafts = drafts


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        profile_file = Path(directory) / "profiles.json"
        profiles = SenderProfileService(profile_file)
        assert profiles.names() == ["Personal"]

        nonprofit = profiles.create("Community Charity")
        profiles.update(
            nonprofit.profile_id,
            sender_name="Alex Example",
            role="Coordinator",
            organisation="Community Charity",
            email="hello@example.org",
            website="https://example.org",
            charity_information="Registered charity example",
            organisation_description="Supports the local community.",
        )
        profiles.set_active(nonprofit.profile_id)
        assert profiles.active_profile.name == "Community Charity"

        service = ResponseService(
            store=MemoryStore(),
            profile_service=profiles,
        )
        record = SimpleNamespace(
            tracking_id="record-1",
            title="Volunteer Program",
            url="https://opportunity.example",
            source="Official website",
        )
        draft = service.get_or_create_draft(record)
        template = service.get_template_by_name("General Enquiry")
        service.apply_template(draft, template, record)
        assert "Alex Example" in draft.body
        assert "Community Charity" in draft.body
        assert "https://example.org" in draft.body
        assert "Registered charity example" in draft.body

        reloaded = SenderProfileService(profile_file)
        assert reloaded.active_profile.name == "Community Charity"
        assert reloaded.active_profile.website == "https://example.org"

    draft_source = (PROJECT_ROOT / "src/ui/draft_window.py").read_text(
        encoding="utf-8"
    )
    assert "Manage Profiles" in draft_source
    assert VERSION_INFO.version == "1.1.0"
    assert VERSION_INFO.package == "Package-110A-01"
    assert VERSION_INFO.build == 1
    print("Sender profiles test passed.")


if __name__ == "__main__":
    main()
