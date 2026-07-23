"""Chronological activity timeline for one opportunity."""

from __future__ import annotations

import customtkinter as ctk


class TimelineWindow(ctk.CTkToplevel):
    def __init__(self, master, tracked_record, service):
        super().__init__(master)
        self.tracked_record = tracked_record
        self.service = service

        self.title("Opportunity Timeline")
        self.geometry("760x700")
        self.minsize(620, 540)
        self.transient(master)
        self.build_ui()
        self.refresh_events()

    def build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(
            self,
            text=self.tracked_record.title,
            font=("Segoe UI", 20, "bold"),
            anchor="w",
            wraplength=690,
        ).grid(row=0, column=0, sticky="ew", padx=15, pady=(15, 8))

        add_row = ctk.CTkFrame(self)
        add_row.grid(row=1, column=0, sticky="ew", padx=15, pady=6)
        add_row.grid_columnconfigure(0, weight=1)
        self.note_entry = ctk.CTkEntry(
            add_row,
            placeholder_text="Add a timeline note",
        )
        self.note_entry.grid(row=0, column=0, sticky="ew", padx=8, pady=8)
        self.note_entry.bind("<Return>", lambda event: self.add_note())
        ctk.CTkButton(
            add_row,
            text="Add Note",
            width=100,
            command=self.add_note,
        ).grid(row=0, column=1, padx=8, pady=8)

        self.event_list = ctk.CTkScrollableFrame(self)
        self.event_list.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=15,
            pady=(6, 15),
        )

    def refresh_events(self):
        for widget in self.event_list.winfo_children():
            widget.destroy()
        events = self.service.for_opportunity(
            self.tracked_record.tracking_id
        )
        if not events:
            ctk.CTkLabel(
                self.event_list,
                text="No timeline events yet.",
                anchor="w",
            ).pack(fill="x", padx=10, pady=12)
            return
        for event in events:
            row = ctk.CTkFrame(self.event_list)
            row.pack(fill="x", padx=5, pady=4)
            row.grid_columnconfigure(0, weight=1)
            display_time = event.event_at.replace("T", " ")[:19]
            details = f"\n{event.details}" if event.details else ""
            ctk.CTkLabel(
                row,
                text=(
                    f"{display_time}  |  {event.event_type}\n"
                    f"{event.title}{details}"
                ),
                justify="left",
                anchor="w",
                wraplength=620,
            ).grid(row=0, column=0, sticky="ew", padx=10, pady=9)

    def add_note(self):
        note = self.note_entry.get().strip()
        if not note:
            return
        self.service.record(
            self.tracked_record.tracking_id,
            "Note",
            "Manual timeline note",
            note,
        )
        self.note_entry.delete(0, "end")
        self.refresh_events()
