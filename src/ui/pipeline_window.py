"""Pipeline dashboard for tracked opportunities."""

from __future__ import annotations

import webbrowser
from tkinter import filedialog

import customtkinter as ctk

from src.tracking.tracked_opportunity import TrackedOpportunity
from src.ui.checklist_window import ChecklistWindow
from src.ui.contact_history_window import ContactHistoryWindow
from src.ui.draft_window import DraftWindow


class PipelineWindow(ctk.CTkToplevel):
    def __init__(self, master, service, export_service):
        super().__init__(master)
        self.service = service
        self.export_service = export_service

        self.title("Opportunity Pipeline")
        self.geometry("1120x780")
        self.minsize(900, 620)
        self.transient(master)
        self.stage_value = ctk.StringVar(value="All")
        self.priority_value = ctk.StringVar(value="All")
        self.build_ui()
        self.refresh_dashboard()

    def build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        header = ctk.CTkFrame(self)
        header.grid(row=0, column=0, sticky="ew", padx=12, pady=(12, 6))
        header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header,
            text="Opportunity Pipeline",
            font=("Segoe UI", 22, "bold"),
        ).grid(row=0, column=0, sticky="w", padx=12, pady=12)

        ctk.CTkOptionMenu(
            header,
            values=["All", *TrackedOpportunity.STATUSES],
            variable=self.stage_value,
            command=lambda value: self.refresh_dashboard(),
            width=130,
        ).grid(row=0, column=1, padx=6, pady=12)

        ctk.CTkOptionMenu(
            header,
            values=["All", "High", "Medium", "Low"],
            variable=self.priority_value,
            command=lambda value: self.refresh_dashboard(),
            width=120,
        ).grid(row=0, column=2, padx=6, pady=12)

        ctk.CTkButton(
            header,
            text="Export CSV",
            width=100,
            command=self.export_csv,
        ).grid(row=0, column=3, padx=6, pady=12)

        ctk.CTkButton(
            header,
            text="Refresh",
            width=90,
            command=self.refresh_dashboard,
        ).grid(row=0, column=4, padx=12, pady=12)

        self.total_frame = ctk.CTkFrame(self)
        self.total_frame.grid(row=1, column=0, sticky="ew", padx=12, pady=6)
        for column in range(len(TrackedOpportunity.STATUSES)):
            self.total_frame.grid_columnconfigure(column, weight=1)

        self.pipeline_list = ctk.CTkScrollableFrame(self)
        self.pipeline_list.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=12,
            pady=(6, 12),
        )

    def refresh_dashboard(self):
        for widget in self.total_frame.winfo_children():
            widget.destroy()
        totals = self.service.stage_totals()
        for column, status in enumerate(TrackedOpportunity.STATUSES):
            card = ctk.CTkFrame(self.total_frame)
            card.grid(row=0, column=column, sticky="ew", padx=5, pady=8)
            ctk.CTkLabel(
                card,
                text=str(totals.get(status, 0)),
                font=("Segoe UI", 22, "bold"),
            ).pack(pady=(8, 0))
            ctk.CTkLabel(card, text=status).pack(pady=(0, 8))

        for widget in self.pipeline_list.winfo_children():
            widget.destroy()
        items = self.service.items(
            stage=self.stage_value.get(),
            priority=self.priority_value.get(),
        )
        if not items:
            ctk.CTkLabel(
                self.pipeline_list,
                text="No opportunities in this pipeline view.",
                anchor="w",
            ).pack(fill="x", padx=12, pady=15)
            return
        for item in items:
            self._add_item(item)

    def _add_item(self, item):
        record = item.record
        card = ctk.CTkFrame(self.pipeline_list)
        card.pack(fill="x", padx=5, pady=5)
        card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            card,
            text=(
                f"{record.title}\n"
                f"Stage: {record.status}   Priority: {item.priority_label}   "
                f"Rating: {record.rating}/5   Score: {record.score}/100\n"
                f"Checklist: {item.checklist_percent}%   "
                f"Draft: {'Saved' if item.has_draft else 'Not started'}   "
                f"Interactions: {item.interaction_count}"
            ),
            justify="left",
            anchor="w",
            font=("Segoe UI", 13, "bold"),
        ).grid(
            row=0,
            column=0,
            columnspan=5,
            sticky="ew",
            padx=12,
            pady=10,
        )

        ctk.CTkButton(
            card,
            text="Checklist",
            width=90,
            command=lambda: self.open_checklist(record),
        ).grid(row=1, column=0, sticky="w", padx=12, pady=(0, 10))
        ctk.CTkButton(
            card,
            text="Draft",
            width=80,
            command=lambda: self.open_draft(record),
        ).grid(row=1, column=1, padx=5, pady=(0, 10))
        ctk.CTkButton(
            card,
            text="Contacts",
            width=85,
            command=lambda: self.open_contacts(record),
        ).grid(row=1, column=2, padx=5, pady=(0, 10))
        ctk.CTkButton(
            card,
            text="Open",
            width=75,
            command=lambda: webbrowser.open(record.url) if record.url else None,
        ).grid(row=1, column=3, padx=(5, 12), pady=(0, 10))

        ctk.CTkButton(
            card,
            text="Report",
            width=80,
            command=lambda: self.export_report(record),
        ).grid(row=1, column=4, padx=(5, 12), pady=(0, 10))

    def open_checklist(self, record):
        workflow = self.master.workflow_service.get_or_create(record)
        ChecklistWindow(
            self,
            workflow,
            self.master.workflow_service,
            record.url,
        )

    def open_draft(self, record):
        DraftWindow(self, record, self.master.response_service)

    def open_contacts(self, record):
        ContactHistoryWindow(self, record, self.master.contact_service)

    def export_csv(self):
        path = filedialog.asksaveasfilename(
            parent=self,
            title="Export Pipeline CSV",
            defaultextension=".csv",
            initialfile="opportunity_pipeline.csv",
            filetypes=[("CSV files", "*.csv")],
        )
        if path:
            self.export_service.export_pipeline(
                path,
                stage=self.stage_value.get(),
                priority=self.priority_value.get(),
            )

    def export_report(self, record):
        path = filedialog.asksaveasfilename(
            parent=self,
            title="Export Opportunity Report",
            defaultextension=".txt",
            initialfile=self.export_service.suggested_report_name(record.title),
            filetypes=[("Text files", "*.txt")],
        )
        if path:
            self.export_service.export_opportunity_report(record, path)
