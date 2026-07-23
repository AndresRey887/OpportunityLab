"""Pipeline dashboard for tracked opportunities."""

from __future__ import annotations

import webbrowser
from tkinter import filedialog

import customtkinter as ctk

from src.tracking.tracked_opportunity import TrackedOpportunity
from src.ui.checklist_window import ChecklistWindow
from src.ui.contact_history_window import ContactHistoryWindow
from src.ui.company_profile_window import CompanyProfileWindow
from src.ui.draft_window import DraftWindow
from src.ui.duplicate_clusters_window import DuplicateClustersWindow
from src.ui.decision_review_window import DecisionReviewWindow
from src.ui.outcome_window import OutcomeWindow
from src.ui.search_memory_window import SearchMemoryWindow
from src.ui.timeline_window import TimelineWindow
from src.ui.market_trends_window import MarketTrendsWindow
from src.ui.social_signals_window import SocialSignalsWindow
from src.ui.product_launches_window import ProductLaunchesWindow
from src.ui.research_workspaces_window import ResearchWorkspacesWindow


class PipelineWindow(ctk.CTkToplevel):
    def __init__(self, master, service, export_service):
        super().__init__(master)
        self.service = service
        self.export_service = export_service
        self.clusters_window = None
        self.search_memory_window = None
        self.decision_review_window = None
        self.market_trends_window = None
        self.social_signals_window = None
        self.product_launches_window = None
        self.research_workspaces_window = None

        self.title("Opportunity Pipeline")
        self.geometry("1400x780")
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
            text="Clusters",
            width=90,
            command=self.open_clusters,
        ).grid(row=0, column=4, padx=6, pady=12)

        ctk.CTkButton(
            header,
            text="Memory",
            width=85,
            command=self.open_search_memory,
        ).grid(row=0, column=5, padx=6, pady=12)

        ctk.CTkButton(
            header,
            text="Review",
            width=80,
            command=self.open_decision_review,
        ).grid(row=0, column=6, padx=6, pady=12)

        ctk.CTkButton(
            header,
            text="Trends",
            width=80,
            command=self.open_market_trends,
        ).grid(row=0, column=7, padx=6, pady=12)

        ctk.CTkButton(
            header,
            text="Signals",
            width=80,
            command=self.open_social_signals,
        ).grid(row=0, column=8, padx=6, pady=12)

        ctk.CTkButton(
            header,
            text="Launches",
            width=85,
            command=self.open_product_launches,
        ).grid(row=0, column=9, padx=6, pady=12)

        ctk.CTkButton(
            header,
            text="Workspaces",
            width=95,
            command=self.open_research_workspaces,
        ).grid(row=0, column=10, padx=6, pady=12)

        ctk.CTkButton(
            header,
            text="Refresh",
            width=90,
            command=self.refresh_dashboard,
        ).grid(row=0, column=11, padx=12, pady=12)

        self.outcome_summary = ctk.CTkLabel(
            header,
            text="",
            anchor="w",
        )
        self.outcome_summary.grid(
            row=1,
            column=0,
            columnspan=12,
            sticky="ew",
            padx=12,
            pady=(0, 10),
        )

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
        outcome_summary = self.master.outcome_service.summary()
        self.outcome_summary.configure(
            text=(
                f"Outcomes recorded: {outcome_summary['recorded']}   "
                f"Successful: {outcome_summary['successful']}   "
                f"Success rate: {outcome_summary['success_rate']}%   "
                f"Successful value: ${outcome_summary['estimated_value']:,.2f}"
            )
        )
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
            columnspan=8,
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

        ctk.CTkButton(
            card,
            text="Outcome",
            width=85,
            command=lambda: self.open_outcome(record),
        ).grid(row=1, column=5, padx=(5, 12), pady=(0, 10))

        ctk.CTkButton(
            card,
            text="Timeline",
            width=85,
            command=lambda: self.open_timeline(record),
        ).grid(row=1, column=6, padx=(5, 12), pady=(0, 10))

        ctk.CTkButton(
            card,
            text="Company",
            width=85,
            command=lambda: self.open_company(record),
        ).grid(row=1, column=7, padx=(5, 12), pady=(0, 10))

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

    def open_outcome(self, record):
        OutcomeWindow(
            self,
            record,
            self.master.outcome_service,
            on_saved=self.refresh_dashboard,
        )

    def open_timeline(self, record):
        TimelineWindow(
            self,
            record,
            self.master.timeline_service,
        )

    def open_company(self, record):
        profile = self.master.company_intelligence_service.get_or_create(record)
        CompanyProfileWindow(
            self,
            profile,
            self.master.company_intelligence_service,
            self.master.tracking_service,
            self.master.research_evidence_service,
            self.master.competitor_service,
        )

    def open_clusters(self):
        if self.clusters_window is not None:
            try:
                if self.clusters_window.winfo_exists():
                    self.clusters_window.refresh_clusters()
                    self.clusters_window.focus()
                    return
            except Exception:
                pass
        self.clusters_window = DuplicateClustersWindow(
            self.master,
            self.master.duplicate_cluster_service,
        )

    def open_search_memory(self):
        if self.search_memory_window is not None:
            try:
                if self.search_memory_window.winfo_exists():
                    self.search_memory_window.refresh_memory()
                    self.search_memory_window.focus()
                    return
            except Exception:
                pass
        self.search_memory_window = SearchMemoryWindow(
            self.master,
            self.master.search_memory_service,
        )

    def open_decision_review(self):
        if self.decision_review_window is not None:
            try:
                if self.decision_review_window.winfo_exists():
                    self.decision_review_window.refresh_review()
                    self.decision_review_window.focus()
                    return
            except Exception:
                pass
        self.decision_review_window = DecisionReviewWindow(
            self.master,
            self.master.decision_review_service,
            self.master.learning_export_service,
        )

    def open_market_trends(self):
        if self.market_trends_window is not None:
            try:
                if self.market_trends_window.winfo_exists():
                    self.market_trends_window.refresh_topics()
                    self.market_trends_window.focus()
                    return
            except Exception:
                pass
        self.market_trends_window = MarketTrendsWindow(
            self.master,
            self.master.trend_service,
        )

    def open_social_signals(self):
        if self.social_signals_window is not None:
            try:
                if self.social_signals_window.winfo_exists():
                    self.social_signals_window.refresh_topics()
                    self.social_signals_window.refresh_signals()
                    self.social_signals_window.focus()
                    return
            except Exception:
                pass
        self.social_signals_window = SocialSignalsWindow(
            self.master,
            self.master.social_signal_service,
            self.master.trend_service,
        )

    def open_product_launches(self):
        if self.product_launches_window is not None:
            try:
                if self.product_launches_window.winfo_exists():
                    self.product_launches_window.refresh_companies()
                    self.product_launches_window.refresh_launches()
                    self.product_launches_window.focus()
                    return
            except Exception:
                pass
        self.product_launches_window = ProductLaunchesWindow(
            self.master,
            self.master.product_launch_service,
            self.master.company_intelligence_service,
        )

    def open_research_workspaces(self):
        if self.research_workspaces_window is not None:
            try:
                if self.research_workspaces_window.winfo_exists():
                    self.research_workspaces_window.refresh()
                    self.research_workspaces_window.focus()
                    return
            except Exception:
                pass
        self.research_workspaces_window = ResearchWorkspacesWindow(
            self.master,
            self.master.research_workspace_service,
            self.master.discovery_brief_service,
        )

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
