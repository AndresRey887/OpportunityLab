"""Add and review sourced company research evidence."""

from __future__ import annotations

import webbrowser
from datetime import date

import customtkinter as ctk

from src.research.research_evidence import ResearchEvidence


class ResearchEvidenceWindow(ctk.CTkToplevel):
    def __init__(self, master, company_profile, service):
        super().__init__(master)
        self.company_profile = company_profile
        self.service = service
        self.title("Company Research Evidence")
        self.geometry("900x780")
        self.minsize(720, 620)
        self.transient(master)
        self.category_filter = ctk.StringVar(value="All")
        self.build_ui()
        self.refresh_evidence()

    def build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        header = ctk.CTkFrame(self)
        header.grid(row=0, column=0, sticky="ew", padx=12, pady=12)
        header.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(
            header,
            text=f"Research Evidence — {self.company_profile.name}",
            font=("Segoe UI", 20, "bold"),
            anchor="w",
        ).grid(row=0, column=0, sticky="ew", padx=12, pady=12)
        ctk.CTkOptionMenu(
            header,
            values=["All", *ResearchEvidence.CATEGORIES],
            variable=self.category_filter,
            command=lambda value: self.refresh_evidence(),
            width=155,
        ).grid(row=0, column=1, padx=12, pady=12)
        self.summary_label = ctk.CTkLabel(header, text="", anchor="w")
        self.summary_label.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=12,
            pady=(0, 10),
        )

        add_frame = ctk.CTkFrame(self)
        add_frame.grid(row=1, column=0, sticky="ew", padx=12, pady=6)
        add_frame.grid_columnconfigure((0, 1), weight=1)
        self.category_value = ctk.StringVar(value="Company Overview")
        ctk.CTkOptionMenu(
            add_frame,
            values=list(ResearchEvidence.CATEGORIES),
            variable=self.category_value,
        ).grid(row=0, column=0, sticky="ew", padx=8, pady=6)
        self.confidence_value = ctk.StringVar(value="3")
        ctk.CTkOptionMenu(
            add_frame,
            values=["1", "2", "3", "4", "5"],
            variable=self.confidence_value,
        ).grid(row=0, column=1, sticky="ew", padx=8, pady=6)
        self.claim_entry = self._entry(
            add_frame,
            "Research finding or claim",
            1,
            0,
            2,
        )
        self.source_title_entry = self._entry(
            add_frame,
            "Source title",
            2,
            0,
        )
        self.source_url_entry = self._entry(
            add_frame,
            "Source URL",
            2,
            1,
        )
        self.date_entry = self._entry(
            add_frame,
            "Evidence date",
            3,
            0,
        )
        self.date_entry.insert(0, date.today().isoformat())
        self.notes_entry = self._entry(
            add_frame,
            "Evidence notes",
            3,
            1,
        )
        ctk.CTkButton(
            add_frame,
            text="Add Evidence",
            command=self.add_evidence,
        ).grid(row=4, column=0, columnspan=2, sticky="ew", padx=8, pady=8)

        self.message = ctk.CTkLabel(self, text="", anchor="w")
        self.message.grid(row=2, column=0, sticky="ew", padx=18, pady=4)

        self.evidence_list = ctk.CTkScrollableFrame(self)
        self.evidence_list.grid(
            row=3,
            column=0,
            sticky="nsew",
            padx=12,
            pady=(4, 12),
        )

    @staticmethod
    def _entry(parent, placeholder, row, column, columnspan=1):
        entry = ctk.CTkEntry(parent, placeholder_text=placeholder)
        entry.grid(
            row=row,
            column=column,
            columnspan=columnspan,
            sticky="ew",
            padx=8,
            pady=5,
        )
        return entry

    def add_evidence(self):
        claim = self.claim_entry.get().strip()
        if not claim:
            self.message.configure(text="Enter a research finding or claim.")
            return
        self.service.add(
            self.company_profile.company_id,
            category=self.category_value.get(),
            claim=claim,
            source_url=self.source_url_entry.get(),
            source_title=self.source_title_entry.get(),
            evidence_date=self.date_entry.get(),
            confidence=self.confidence_value.get(),
            notes=self.notes_entry.get(),
        )
        for entry in (
            self.claim_entry,
            self.source_title_entry,
            self.source_url_entry,
            self.notes_entry,
        ):
            entry.delete(0, "end")
        self.message.configure(text="Research evidence saved.")
        self.refresh_evidence()

    def refresh_evidence(self):
        for widget in self.evidence_list.winfo_children():
            widget.destroy()
        summary = self.service.summary(self.company_profile.company_id)
        self.summary_label.configure(
            text=(
                f"Evidence: {summary['total']}   "
                f"High confidence: {summary['high_confidence']}   "
                f"With sources: {summary['sourced']}   "
                f"Categories: {summary['categories']}"
            )
        )
        items = self.service.for_company(
            self.company_profile.company_id,
            self.category_filter.get(),
        )
        if not items:
            ctk.CTkLabel(
                self.evidence_list,
                text="No research evidence in this view.",
                anchor="w",
            ).pack(fill="x", padx=10, pady=12)
            return
        for item in items:
            row = ctk.CTkFrame(self.evidence_list)
            row.pack(fill="x", padx=5, pady=5)
            row.grid_columnconfigure(0, weight=1)
            source = item.source_title or item.source_url or "No source link"
            notes = f"\nNotes: {item.notes}" if item.notes else ""
            ctk.CTkLabel(
                row,
                text=(
                    f"{item.category}   {item.evidence_date}   "
                    f"Confidence: {item.confidence}/5\n"
                    f"{item.claim}\nSource: {source}{notes}"
                ),
                justify="left",
                anchor="w",
                wraplength=680,
            ).grid(row=0, column=0, sticky="ew", padx=10, pady=8)
            ctk.CTkButton(
                row,
                text="Open Source",
                width=95,
                state="normal" if item.source_url else "disabled",
                command=lambda value=item.source_url: webbrowser.open(value),
            ).grid(row=0, column=1, padx=5, pady=8)
            ctk.CTkButton(
                row,
                text="Remove",
                width=75,
                command=lambda value=item.evidence_id: self.remove_evidence(value),
            ).grid(row=0, column=2, padx=(5, 10), pady=8)

    def remove_evidence(self, evidence_id):
        self.service.remove(evidence_id)
        self.message.configure(text="Research evidence removed.")
        self.refresh_evidence()
