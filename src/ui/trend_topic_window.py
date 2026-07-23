"""Add and review dated observations for one market topic."""

from __future__ import annotations

import webbrowser
from datetime import date

import customtkinter as ctk

from src.trends.trend_observation import TrendObservation


class TrendTopicWindow(ctk.CTkToplevel):
    def __init__(self, master, topic, service, on_change=None):
        super().__init__(master)
        self.topic = topic
        self.service = service
        self.on_change = on_change
        self.title("Trend Observations")
        self.geometry("900x780")
        self.minsize(720, 620)
        self.transient(master)
        self.build_ui()
        self.refresh_observations()

    def build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        ctk.CTkLabel(
            self,
            text=self.topic.name,
            font=("Segoe UI", 21, "bold"),
            anchor="w",
        ).grid(row=0, column=0, sticky="ew", padx=15, pady=(15, 8))

        add_frame = ctk.CTkFrame(self)
        add_frame.grid(row=1, column=0, sticky="ew", padx=15, pady=6)
        add_frame.grid_columnconfigure((0, 1), weight=1)
        self.direction_value = ctk.StringVar(value="Rising")
        ctk.CTkOptionMenu(
            add_frame,
            values=list(TrendObservation.DIRECTIONS),
            variable=self.direction_value,
        ).grid(row=0, column=0, sticky="ew", padx=8, pady=6)
        self.strength_value = ctk.StringVar(value="3")
        ctk.CTkOptionMenu(
            add_frame,
            values=["1", "2", "3", "4", "5"],
            variable=self.strength_value,
        ).grid(row=0, column=1, sticky="ew", padx=8, pady=6)
        self.summary_entry = self._entry(
            add_frame,
            "What changed or was observed?",
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
            "Observation date",
            3,
            0,
        )
        self.date_entry.insert(0, date.today().isoformat())
        self.notes_entry = self._entry(
            add_frame,
            "Notes",
            3,
            1,
        )
        ctk.CTkButton(
            add_frame,
            text="Add Observation",
            command=self.add_observation,
        ).grid(row=4, column=0, columnspan=2, sticky="ew", padx=8, pady=8)

        self.summary_label = ctk.CTkLabel(self, text="", anchor="w")
        self.summary_label.grid(row=2, column=0, sticky="ew", padx=18, pady=6)

        self.observation_list = ctk.CTkScrollableFrame(self)
        self.observation_list.grid(
            row=3,
            column=0,
            sticky="nsew",
            padx=15,
            pady=(6, 15),
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

    def add_observation(self):
        summary = self.summary_entry.get().strip()
        if not summary:
            return
        self.service.add_observation(
            self.topic.topic_id,
            direction=self.direction_value.get(),
            strength=self.strength_value.get(),
            summary=summary,
            observation_date=self.date_entry.get(),
            source_title=self.source_title_entry.get(),
            source_url=self.source_url_entry.get(),
            notes=self.notes_entry.get(),
        )
        for entry in (
            self.summary_entry,
            self.source_title_entry,
            self.source_url_entry,
            self.notes_entry,
        ):
            entry.delete(0, "end")
        self.refresh_observations()
        if self.on_change:
            self.on_change()

    def refresh_observations(self):
        for widget in self.observation_list.winfo_children():
            widget.destroy()
        summary = self.service.summary(self.topic.topic_id)
        self.summary_label.configure(
            text=(
                f"Latest: {summary['latest_direction']}   "
                f"Observations: {summary['observations']}   "
                f"Average strength: {summary['average_strength']}/5   "
                f"Momentum: {summary['momentum']}   "
                f"With sources: {summary['sourced']}"
            )
        )
        items = self.service.for_topic(self.topic.topic_id)
        if not items:
            ctk.CTkLabel(
                self.observation_list,
                text="No observations yet.",
                anchor="w",
            ).pack(fill="x", padx=10, pady=12)
            return
        for item in items:
            row = ctk.CTkFrame(self.observation_list)
            row.pack(fill="x", padx=5, pady=5)
            row.grid_columnconfigure(0, weight=1)
            source = item.source_title or item.source_url or "No source"
            ctk.CTkLabel(
                row,
                text=(
                    f"{item.observation_date}   {item.direction}   "
                    f"Strength: {item.strength}/5\n"
                    f"{item.summary}\nSource: {source}"
                ),
                justify="left",
                anchor="w",
                wraplength=670,
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
                command=lambda value=item.observation_id: self.remove_observation(value),
            ).grid(row=0, column=2, padx=(5, 10), pady=8)

    def remove_observation(self, observation_id):
        self.service.remove_observation(observation_id)
        self.refresh_observations()
        if self.on_change:
            self.on_change()
