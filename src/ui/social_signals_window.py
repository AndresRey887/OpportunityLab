"""Add and review social signals across discovery sources."""

from __future__ import annotations

import webbrowser
from datetime import date

import customtkinter as ctk

from src.signals.social_signal import SocialSignal


class SocialSignalsWindow(ctk.CTkToplevel):
    def __init__(self, master, service, trend_service):
        super().__init__(master)
        self.service = service
        self.trend_service = trend_service
        self.title("Social Signals")
        self.geometry("950x800")
        self.minsize(760, 620)
        self.transient(master)
        self.platform_filter = ctk.StringVar(value="All")
        self.topic_names = {}
        self.build_ui()
        self.refresh_topics()
        self.refresh_signals()

    def build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)
        header = ctk.CTkFrame(self)
        header.grid(row=0, column=0, sticky="ew", padx=12, pady=12)
        header.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(
            header, text="Social Signals", font=("Segoe UI", 22, "bold"), anchor="w"
        ).grid(row=0, column=0, sticky="ew", padx=12, pady=12)
        ctk.CTkOptionMenu(
            header,
            values=["All", *SocialSignal.PLATFORMS],
            variable=self.platform_filter,
            command=lambda value: self.refresh_signals(),
            width=150,
        ).grid(row=0, column=1, padx=12, pady=12)
        self.summary_label = ctk.CTkLabel(header, text="", anchor="w")
        self.summary_label.grid(row=1, column=0, columnspan=2, sticky="ew", padx=12, pady=(0, 10))

        form = ctk.CTkFrame(self)
        form.grid(row=1, column=0, sticky="ew", padx=12, pady=6)
        form.grid_columnconfigure((0, 1), weight=1)
        self.platform_value = ctk.StringVar(value="Reddit")
        ctk.CTkOptionMenu(form, values=list(SocialSignal.PLATFORMS), variable=self.platform_value).grid(row=0, column=0, sticky="ew", padx=8, pady=5)
        self.sentiment_value = ctk.StringVar(value="Neutral")
        ctk.CTkOptionMenu(form, values=list(SocialSignal.SENTIMENTS), variable=self.sentiment_value).grid(row=0, column=1, sticky="ew", padx=8, pady=5)
        self.strength_value = ctk.StringVar(value="3")
        ctk.CTkOptionMenu(form, values=["1", "2", "3", "4", "5"], variable=self.strength_value).grid(row=0, column=2, padx=8, pady=5)
        self.topic_value = ctk.StringVar(value="No topic")
        self.topic_menu = ctk.CTkOptionMenu(form, values=["No topic"], variable=self.topic_value)
        self.topic_menu.grid(row=0, column=3, padx=8, pady=5)
        self.title_entry = self._entry(form, "Signal title", 1, 0, 2)
        self.summary_entry = self._entry(form, "What does the signal indicate?", 1, 2, 2)
        self.url_entry = self._entry(form, "Source URL", 2, 0, 2)
        self.date_entry = self._entry(form, "Signal date", 2, 2)
        self.date_entry.insert(0, date.today().isoformat())
        self.notes_entry = self._entry(form, "Notes", 2, 3)
        ctk.CTkButton(form, text="Add Signal", command=self.add_signal).grid(row=3, column=0, columnspan=4, sticky="ew", padx=8, pady=8)

        self.message = ctk.CTkLabel(self, text="", anchor="w")
        self.message.grid(row=2, column=0, sticky="ew", padx=18, pady=4)
        self.signal_list = ctk.CTkScrollableFrame(self)
        self.signal_list.grid(row=3, column=0, sticky="nsew", padx=12, pady=(4, 12))

    @staticmethod
    def _entry(parent, placeholder, row, column, columnspan=1):
        entry = ctk.CTkEntry(parent, placeholder_text=placeholder)
        entry.grid(row=row, column=column, columnspan=columnspan, sticky="ew", padx=8, pady=5)
        return entry

    def refresh_topics(self):
        self.topic_names = {"No topic": ""}
        self.topic_names.update({topic.name: topic.topic_id for topic in self.trend_service.topics})
        self.topic_menu.configure(values=list(self.topic_names))
        self.topic_value.set("No topic")

    def add_signal(self):
        title, summary = self.title_entry.get().strip(), self.summary_entry.get().strip()
        if not title or not summary:
            self.message.configure(text="Enter a signal title and summary.")
            return
        self.service.add(
            platform=self.platform_value.get(),
            title=title,
            summary=summary,
            sentiment=self.sentiment_value.get(),
            strength=int(self.strength_value.get()),
            signal_date=self.date_entry.get(),
            source_url=self.url_entry.get(),
            topic_id=self.topic_names.get(self.topic_value.get(), ""),
            notes=self.notes_entry.get(),
        )
        for entry in (self.title_entry, self.summary_entry, self.url_entry, self.notes_entry):
            entry.delete(0, "end")
        self.message.configure(text="Social signal saved.")
        self.refresh_signals()

    def refresh_signals(self):
        for widget in self.signal_list.winfo_children():
            widget.destroy()
        summary = self.service.summary()
        self.summary_label.configure(text=f"Signals: {summary['total']}   Positive: {summary['positive']}   Negative: {summary['negative']}   Average strength: {summary['average_strength']}/5   Top platform: {summary['top_platform']}")
        for item in self.service.all(self.platform_filter.get()):
            row = ctk.CTkFrame(self.signal_list)
            row.pack(fill="x", padx=5, pady=5)
            row.grid_columnconfigure(0, weight=1)
            ctk.CTkLabel(
                row,
                text=f"{item.signal_date}   {item.platform}   {item.sentiment}   Strength: {item.strength}/5\n{item.title}\n{item.summary}",
                justify="left", anchor="w", wraplength=720,
            ).grid(row=0, column=0, sticky="ew", padx=10, pady=8)
            ctk.CTkButton(row, text="Open Source", width=95, state="normal" if item.source_url else "disabled", command=lambda value=item.source_url: webbrowser.open(value)).grid(row=0, column=1, padx=5, pady=8)
            ctk.CTkButton(row, text="Remove", width=75, command=lambda value=item.signal_id: self.remove_signal(value)).grid(row=0, column=2, padx=(5, 10), pady=8)

    def remove_signal(self, signal_id):
        self.service.remove(signal_id)
        self.refresh_signals()
