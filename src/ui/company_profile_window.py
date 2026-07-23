"""Edit intelligence for one company and view linked opportunities."""

from __future__ import annotations

import webbrowser

import customtkinter as ctk
from src.ui.research_evidence_window import ResearchEvidenceWindow
from src.ui.company_comparison_window import CompanyComparisonWindow


class CompanyProfileWindow(ctk.CTkToplevel):
    def __init__(
        self,
        master,
        profile,
        service,
        tracking_service,
        evidence_service,
        competitor_service,
    ):
        super().__init__(master)
        self.profile = profile
        self.service = service
        self.tracking_service = tracking_service
        self.evidence_service = evidence_service
        self.competitor_service = competitor_service

        self.title("Company Intelligence")
        self.geometry("820x760")
        self.minsize(680, 600)
        self.transient(master)
        self.build_ui()
        self.load_profile()

    def build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        ctk.CTkLabel(
            self,
            text="Company Intelligence",
            font=("Segoe UI", 22, "bold"),
            anchor="w",
        ).grid(row=0, column=0, sticky="ew", padx=15, pady=(15, 8))

        fields = ctk.CTkFrame(self)
        fields.grid(row=1, column=0, sticky="ew", padx=15, pady=6)
        fields.grid_columnconfigure((0, 1), weight=1)
        self.name_entry = self._entry(fields, "Company name", 0, 0)
        self.industry_entry = self._entry(fields, "Industry", 0, 1)
        self.website_entry = self._entry(fields, "Website", 1, 0)
        self.location_entry = self._entry(fields, "Location", 1, 1)
        self.email_entry = self._entry(fields, "Email", 2, 0)
        self.phone_entry = self._entry(fields, "Phone", 2, 1)
        self.tags_entry = self._entry(fields, "Tags, separated by commas", 3, 0, 2)

        text_area = ctk.CTkFrame(self)
        text_area.grid(row=2, column=0, sticky="ew", padx=15, pady=6)
        text_area.grid_columnconfigure((0, 1), weight=1)
        ctk.CTkLabel(
            text_area,
            text="Company description",
            anchor="w",
            font=("Segoe UI", 13, "bold"),
        ).grid(row=0, column=0, sticky="ew", padx=8, pady=(8, 3))
        ctk.CTkLabel(
            text_area,
            text="Research notes",
            anchor="w",
            font=("Segoe UI", 13, "bold"),
        ).grid(row=0, column=1, sticky="ew", padx=8, pady=(8, 3))
        self.description_text = ctk.CTkTextbox(text_area, height=130, wrap="word")
        self.description_text.grid(row=1, column=0, sticky="ew", padx=8, pady=(3, 8))
        self.notes_text = ctk.CTkTextbox(text_area, height=130, wrap="word")
        self.notes_text.grid(row=1, column=1, sticky="ew", padx=8, pady=(3, 8))

        linked_frame = ctk.CTkFrame(self)
        linked_frame.grid(row=3, column=0, sticky="nsew", padx=15, pady=6)
        linked_frame.grid_columnconfigure(0, weight=1)
        linked_frame.grid_rowconfigure(1, weight=1)
        self.linked_summary = ctk.CTkLabel(
            linked_frame,
            text="",
            font=("Segoe UI", 14, "bold"),
            anchor="w",
        )
        self.linked_summary.grid(row=0, column=0, sticky="ew", padx=10, pady=8)
        self.linked_list = ctk.CTkScrollableFrame(linked_frame)
        self.linked_list.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0, 8))

        footer = ctk.CTkFrame(self)
        footer.grid(row=4, column=0, sticky="ew", padx=15, pady=(6, 15))
        footer.grid_columnconfigure(0, weight=1)
        self.message = ctk.CTkLabel(footer, text="", anchor="w")
        self.message.grid(row=0, column=0, sticky="ew", padx=8, pady=8)
        ctk.CTkButton(
            footer,
            text="Competitors",
            command=self.open_competitors,
        ).grid(row=0, column=1, padx=5, pady=8)
        ctk.CTkButton(
            footer,
            text="Research Evidence",
            command=self.open_research_evidence,
        ).grid(row=0, column=2, padx=5, pady=8)
        ctk.CTkButton(
            footer,
            text="Open Website",
            command=self.open_website,
        ).grid(row=0, column=3, padx=5, pady=8)
        ctk.CTkButton(
            footer,
            text="Save Company",
            command=self.save_profile,
        ).grid(row=0, column=4, padx=8, pady=8)

    @staticmethod
    def _entry(parent, placeholder, row, column, columnspan=1):
        entry = ctk.CTkEntry(parent, placeholder_text=placeholder)
        entry.grid(
            row=row,
            column=column,
            columnspan=columnspan,
            sticky="ew",
            padx=8,
            pady=6,
        )
        return entry

    def load_profile(self):
        values = (
            (self.name_entry, self.profile.name),
            (self.industry_entry, self.profile.industry),
            (self.website_entry, self.profile.website),
            (self.location_entry, self.profile.location),
            (self.email_entry, self.profile.email),
            (self.phone_entry, self.profile.phone),
            (self.tags_entry, ", ".join(self.profile.tags)),
        )
        for entry, value in values:
            entry.delete(0, "end")
            entry.insert(0, value)
        self.description_text.delete("1.0", "end")
        self.description_text.insert("1.0", self.profile.description)
        self.notes_text.delete("1.0", "end")
        self.notes_text.insert("1.0", self.profile.notes)
        self.refresh_linked()

    def refresh_linked(self):
        for widget in self.linked_list.winfo_children():
            widget.destroy()
        records = []
        for tracking_id in self.profile.linked_tracking_ids:
            try:
                records.append(self.tracking_service.get(tracking_id))
            except KeyError:
                continue
        self.linked_summary.configure(
            text=f"Linked opportunities: {len(records)}"
        )
        for record in records:
            row = ctk.CTkFrame(self.linked_list)
            row.pack(fill="x", padx=5, pady=4)
            row.grid_columnconfigure(0, weight=1)
            ctk.CTkLabel(
                row,
                text=(
                    f"{record.title}\n"
                    f"{record.status}   Score: {record.score}/100"
                ),
                justify="left",
                anchor="w",
            ).grid(row=0, column=0, sticky="ew", padx=10, pady=8)
            ctk.CTkButton(
                row,
                text="Open",
                width=75,
                command=lambda item=record: webbrowser.open(item.url),
            ).grid(row=0, column=1, padx=8, pady=8)

    def save_profile(self):
        self.profile = self.service.update(
            self.profile.company_id,
            name=self.name_entry.get(),
            industry=self.industry_entry.get(),
            website=self.website_entry.get(),
            location=self.location_entry.get(),
            email=self.email_entry.get(),
            phone=self.phone_entry.get(),
            tags=self.tags_entry.get(),
            description=self.description_text.get("1.0", "end"),
            notes=self.notes_text.get("1.0", "end"),
        )
        self.message.configure(text="Company intelligence saved.")

    def open_website(self):
        url = self.website_entry.get().strip()
        if url:
            webbrowser.open(url)

    def open_research_evidence(self):
        ResearchEvidenceWindow(
            self,
            self.profile,
            self.evidence_service,
        )

    def open_competitors(self):
        CompanyComparisonWindow(
            self,
            self.profile,
            self.service,
            self.competitor_service,
            self.evidence_service,
        )
