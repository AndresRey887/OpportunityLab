"""Manage competitors and compare company intelligence side by side."""

from __future__ import annotations

import webbrowser

import customtkinter as ctk


class CompanyComparisonWindow(ctk.CTkToplevel):
    def __init__(
        self,
        master,
        company_profile,
        company_service,
        competitor_service,
        evidence_service,
    ):
        super().__init__(master)
        self.company_profile = company_profile
        self.company_service = company_service
        self.competitor_service = competitor_service
        self.evidence_service = evidence_service
        self.title("Company Competitors")
        self.geometry("1040x780")
        self.minsize(820, 620)
        self.transient(master)
        self.company_names = {}
        self.build_ui()
        self.refresh_companies()
        self.refresh_comparisons()

    def build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        ctk.CTkLabel(
            self,
            text=f"Competitor Comparison — {self.company_profile.name}",
            font=("Segoe UI", 21, "bold"),
            anchor="w",
        ).grid(row=0, column=0, sticky="ew", padx=15, pady=(15, 8))

        add_row = ctk.CTkFrame(self)
        add_row.grid(row=1, column=0, sticky="ew", padx=15, pady=6)
        add_row.grid_columnconfigure(0, weight=1)
        self.company_value = ctk.StringVar(value="")
        self.company_menu = ctk.CTkOptionMenu(
            add_row,
            values=["No other companies"],
            variable=self.company_value,
        )
        self.company_menu.grid(row=0, column=0, sticky="ew", padx=8, pady=8)
        self.strength_value = ctk.StringVar(value="3")
        ctk.CTkOptionMenu(
            add_row,
            values=["1", "2", "3", "4", "5"],
            variable=self.strength_value,
            width=80,
        ).grid(row=0, column=1, padx=6, pady=8)
        self.overlap_entry = ctk.CTkEntry(
            add_row,
            placeholder_text="Market overlap",
            width=180,
        )
        self.overlap_entry.grid(row=0, column=2, padx=6, pady=8)
        self.notes_entry = ctk.CTkEntry(
            add_row,
            placeholder_text="Comparison notes",
            width=200,
        )
        self.notes_entry.grid(row=0, column=3, padx=6, pady=8)
        ctk.CTkButton(
            add_row,
            text="Save Competitor",
            width=120,
            command=self.save_competitor,
        ).grid(row=0, column=4, padx=8, pady=8)

        self.message = ctk.CTkLabel(self, text="", anchor="w")
        self.message.grid(row=2, column=0, sticky="ew", padx=18, pady=4)

        self.comparison_list = ctk.CTkScrollableFrame(self)
        self.comparison_list.grid(
            row=3,
            column=0,
            sticky="nsew",
            padx=15,
            pady=(4, 15),
        )

    def refresh_companies(self):
        profiles = [
            profile for profile in self.company_service.profiles
            if profile.company_id != self.company_profile.company_id
        ]
        self.company_names = {
            f"{profile.name} — {profile.domain or 'no domain'}": profile
            for profile in profiles
        }
        values = list(self.company_names) or ["No other companies"]
        self.company_menu.configure(values=values)
        self.company_value.set(values[0])

    def save_competitor(self):
        competitor = self.company_names.get(self.company_value.get())
        if competitor is None:
            self.message.configure(
                text="Create another company profile before adding a competitor."
            )
            return
        _, created = self.competitor_service.link(
            self.company_profile.company_id,
            competitor.company_id,
            market_overlap=self.overlap_entry.get(),
            strength=self.strength_value.get(),
            notes=self.notes_entry.get(),
        )
        self.message.configure(
            text=(
                "Competitor added."
                if created
                else "Competitor comparison updated."
            )
        )
        self.refresh_comparisons()

    def refresh_comparisons(self):
        for widget in self.comparison_list.winfo_children():
            widget.destroy()
        comparisons = self.competitor_service.comparisons(
            self.company_profile.company_id,
            self.company_service,
            self.evidence_service,
        )
        if not comparisons:
            ctk.CTkLabel(
                self.comparison_list,
                text="No competitors linked to this company.",
                anchor="w",
            ).pack(fill="x", padx=10, pady=12)
            return
        for comparison in comparisons:
            self._add_comparison(comparison)

    def _add_comparison(self, comparison):
        card = ctk.CTkFrame(self.comparison_list)
        card.pack(fill="x", padx=5, pady=7)
        card.grid_columnconfigure((0, 1), weight=1)

        self._company_column(
            card,
            0,
            comparison.company,
            comparison.company_evidence,
        )
        self._company_column(
            card,
            1,
            comparison.competitor,
            comparison.competitor_evidence,
        )
        ctk.CTkLabel(
            card,
            text=(
                f"Competitive strength: {comparison.link.strength}/5   "
                f"Market overlap: {comparison.link.market_overlap or 'Not set'}\n"
                f"Notes: {comparison.link.notes or 'None'}"
            ),
            justify="left",
            anchor="w",
        ).grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=10,
            pady=8,
        )
        ctk.CTkButton(
            card,
            text="Remove Competitor",
            width=130,
            command=lambda value=comparison.link.link_id: self.remove_link(value),
        ).grid(row=2, column=1, sticky="e", padx=10, pady=(0, 10))

    @staticmethod
    def _company_column(parent, column, profile, evidence):
        frame = ctk.CTkFrame(parent)
        frame.grid(row=0, column=column, sticky="nsew", padx=6, pady=6)
        ctk.CTkLabel(
            frame,
            text=(
                f"{profile.name}\n"
                f"Industry: {profile.industry or 'Not set'}\n"
                f"Location: {profile.location or 'Not set'}\n"
                f"Linked opportunities: {len(profile.linked_tracking_ids)}\n"
                f"Evidence: {evidence['total']} "
                f"({evidence['high_confidence']} high confidence)"
            ),
            font=("Segoe UI", 13, "bold"),
            justify="left",
            anchor="w",
        ).pack(fill="x", padx=10, pady=9)
        ctk.CTkButton(
            frame,
            text="Open Website",
            state="normal" if profile.website else "disabled",
            command=lambda: webbrowser.open(profile.website),
        ).pack(anchor="w", padx=10, pady=(0, 9))

    def remove_link(self, link_id):
        self.competitor_service.remove(link_id)
        self.message.configure(text="Competitor removed.")
        self.refresh_comparisons()
