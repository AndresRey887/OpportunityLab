"""Window for managing tracked opportunities."""

from __future__ import annotations

import webbrowser
from tkinter import messagebox

import customtkinter as ctk

from src.tracking.tracked_opportunity import TrackedOpportunity
from src.ui.checklist_window import ChecklistWindow
from src.ui.draft_window import DraftWindow


class TrackingWindow(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Tracked Opportunities")
        self.geometry("980x760")
        self.minsize(820, 620)
        self.transient(master)

        self.service = master.tracking_service
        self.reminder_service = master.reminder_service
        self.status_filter = ctk.StringVar(value="All")
        self.build_ui()
        self.refresh_records()

    def build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        header = ctk.CTkFrame(self)
        header.grid(row=0, column=0, sticky="ew", padx=12, pady=12)
        header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header,
            text="Tracked Opportunities",
            font=("Segoe UI", 21, "bold"),
        ).grid(row=0, column=0, sticky="w", padx=12, pady=12)

        ctk.CTkOptionMenu(
            header,
            values=["All", *TrackedOpportunity.STATUSES],
            variable=self.status_filter,
            command=lambda selection: self.refresh_records(),
            width=130,
        ).grid(row=0, column=1, padx=12, pady=12)

        self.reminder_summary = ctk.CTkLabel(
            header,
            text="",
            anchor="w",
        )
        self.reminder_summary.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=12,
            pady=(0, 10),
        )

        self.record_list = ctk.CTkScrollableFrame(self)
        self.record_list.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=12,
            pady=(0, 8),
        )

        self.message = ctk.CTkLabel(self, text="", anchor="w")
        self.message.grid(row=2, column=0, sticky="ew", padx=18, pady=(0, 12))

    def refresh_records(self):
        for widget in self.record_list.winfo_children():
            widget.destroy()

        due_count = len(self.reminder_service.due())
        upcoming_count = len(self.reminder_service.upcoming(days=7))
        self.reminder_summary.configure(
            text=(
                f"Due or overdue: {due_count}   "
                f"Coming in 7 days: {upcoming_count}"
            )
        )

        records = self.service.all(self.status_filter.get())
        if not records:
            ctk.CTkLabel(
                self.record_list,
                text="No tracked opportunities in this view.",
                anchor="w",
            ).pack(fill="x", padx=12, pady=15)
            return

        for record in records:
            self._add_record(record)

    def _add_record(self, record):
        card = ctk.CTkFrame(self.record_list)
        card.pack(fill="x", padx=5, pady=6)
        card.grid_columnconfigure(0, weight=1)

        follow_up_text = (
            f"   Follow-up: {record.follow_up_date}"
            if record.follow_up_date
            else ""
        )

        ctk.CTkLabel(
            card,
            text=(
                f"{record.title}\n"
                f"{record.source}   Score: {record.score}/100"
                f"{follow_up_text}"
            ),
            justify="left",
            anchor="w",
            font=("Segoe UI", 14, "bold"),
        ).grid(row=0, column=0, columnspan=6, sticky="ew", padx=12, pady=(10, 6))

        status_value = ctk.StringVar(value=record.status)
        ctk.CTkOptionMenu(
            card,
            values=list(TrackedOpportunity.STATUSES),
            variable=status_value,
            command=lambda value, item=record: self.update_status(item.tracking_id, value),
            width=120,
        ).grid(row=1, column=0, sticky="w", padx=12, pady=5)

        rating_value = ctk.StringVar(value=str(record.rating))
        ctk.CTkOptionMenu(
            card,
            values=["0", "1", "2", "3", "4", "5"],
            variable=rating_value,
            command=lambda value, item=record: self.update_rating(item.tracking_id, value),
            width=75,
        ).grid(row=1, column=1, sticky="w", padx=5, pady=5)

        ctk.CTkButton(
            card,
            text="Checklist",
            width=82,
            command=lambda item=record: self.open_checklist(item),
        ).grid(row=1, column=2, padx=5, pady=5)

        ctk.CTkButton(
            card,
            text="Draft",
            width=75,
            command=lambda item=record: self.open_draft(item),
        ).grid(row=1, column=3, padx=5, pady=5)

        ctk.CTkButton(
            card,
            text="Open",
            width=75,
            command=lambda url=record.url: self.open_url(url),
        ).grid(row=1, column=4, padx=5, pady=5)

        ctk.CTkButton(
            card,
            text="Remove",
            width=80,
            fg_color="#A33A3A",
            hover_color="#7F2D2D",
            command=lambda item=record: self.remove_record(item),
        ).grid(row=1, column=5, padx=(5, 12), pady=5)

        notes_entry = ctk.CTkEntry(card, placeholder_text="Notes")
        notes_entry.insert(0, record.notes)
        notes_entry.grid(row=2, column=0, columnspan=5, sticky="ew", padx=12, pady=5)

        follow_up_entry = ctk.CTkEntry(
            card,
            placeholder_text="Follow-up date, for example 2026-08-15",
        )
        follow_up_entry.insert(0, record.follow_up_date)
        follow_up_entry.grid(row=3, column=0, columnspan=5, sticky="ew", padx=12, pady=(5, 10))

        ctk.CTkButton(
            card,
            text="Save Details",
            width=100,
            command=lambda item=record, notes=notes_entry, follow=follow_up_entry: self.save_details(
                item.tracking_id,
                notes.get(),
                follow.get(),
            ),
        ).grid(row=2, column=5, rowspan=2, padx=(5, 12), pady=(5, 10))

    def open_checklist(self, record):
        workflow = self.master.workflow_service.get_or_create(record)
        ChecklistWindow(
            self,
            workflow,
            self.master.workflow_service,
            record.url,
        )

    def open_draft(self, record):
        DraftWindow(
            self,
            record,
            self.master.response_service,
        )

    def update_status(self, tracking_id, status):
        self.service.update(tracking_id, status=status)
        self.message.configure(text="Status saved.")

    def update_rating(self, tracking_id, rating):
        self.service.update(tracking_id, rating=int(rating))
        self.message.configure(text="Rating saved.")

    def save_details(self, tracking_id, notes, follow_up_date):
        self.service.update(
            tracking_id,
            notes=notes,
            follow_up_date=follow_up_date,
        )
        self.message.configure(text="Notes and follow-up saved.")
        self.master.refresh_tracking_notice()
        self.refresh_records()

    def remove_record(self, record):
        if not messagebox.askyesno(
            "Remove Tracked Opportunity",
            f"Remove '{record.title}' from tracking?",
            parent=self,
        ):
            return
        self.service.remove(record.tracking_id)
        self.message.configure(text="Tracked opportunity removed.")
        self.master.refresh_tracking_notice()
        self.refresh_records()

    @staticmethod
    def open_url(url):
        if url:
            webbrowser.open(url)
