"""Manage contact details and dated interaction histories."""

from __future__ import annotations

from src.contacts.contact_record import ContactRecord
from src.contacts.contact_store import ContactStore
from src.contacts.interaction_entry import InteractionEntry


class ContactService:
    def __init__(self, store: ContactStore | None = None) -> None:
        self.store = store or ContactStore()
        self.contacts = self.store.load_contacts()
        self.interactions = self.store.load_interactions()

    def get_or_create_contact(self, record) -> ContactRecord:
        for contact in self.contacts:
            if contact.tracking_id == record.tracking_id:
                return contact
        contact = ContactRecord(
            tracking_id=record.tracking_id,
            opportunity_title=record.title,
            website=record.url,
        )
        self.contacts.append(contact)
        self.store.save_contacts(self.contacts)
        return contact

    def update_contact(self, tracking_id: str, **values) -> ContactRecord:
        contact = self.get_contact(tracking_id)
        for field_name in (
            "contact_name",
            "organisation",
            "email",
            "phone",
            "website",
            "notes",
        ):
            if field_name in values:
                setattr(contact, field_name, str(values[field_name]).strip())
        contact.touch()
        self.store.save_contacts(self.contacts)
        return contact

    def get_contact(self, tracking_id: str) -> ContactRecord:
        for contact in self.contacts:
            if contact.tracking_id == tracking_id:
                return contact
        raise KeyError(tracking_id)

    def history(self, tracking_id: str) -> list[InteractionEntry]:
        return sorted(
            (
                item
                for item in self.interactions
                if item.tracking_id == tracking_id
            ),
            key=lambda item: (item.interaction_date, item.created_at),
            reverse=True,
        )

    def add_interaction(
        self,
        tracking_id: str,
        interaction_type: str,
        summary: str,
        interaction_date: str,
    ) -> InteractionEntry:
        entry = InteractionEntry(
            tracking_id=tracking_id,
            interaction_type=interaction_type,
            summary=summary,
            interaction_date=interaction_date,
        )
        self.interactions.append(entry)
        self.store.save_interactions(self.interactions)
        return entry

    def remove_interaction(self, entry_id: str) -> None:
        original_count = len(self.interactions)
        self.interactions = [
            item for item in self.interactions
            if item.entry_id != entry_id
        ]
        if len(self.interactions) == original_count:
            raise KeyError(entry_id)
        self.store.save_interactions(self.interactions)
