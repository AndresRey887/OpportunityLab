"""Create and review market topics monitored over time."""

from __future__ import annotations

import customtkinter as ctk

from src.trends.market_topic import MarketTopic
from src.ui.trend_topic_window import TrendTopicWindow


class MarketTrendsWindow(ctk.CTkToplevel):
    def __init__(self, master, service):
        super().__init__(master)
        self.service = service
        self.title("Market Trends")
        self.geometry("900x720")
        self.minsize(720, 560)
        self.transient(master)
        self.build_ui()
        self.refresh_topics()

    def build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(
            self,
            text="Market Trends",
            font=("Segoe UI", 22, "bold"),
            anchor="w",
        ).grid(row=0, column=0, sticky="ew", padx=15, pady=(15, 8))

        add_row = ctk.CTkFrame(self)
        add_row.grid(row=1, column=0, sticky="ew", padx=15, pady=6)
        add_row.grid_columnconfigure(0, weight=1)
        self.name_entry = ctk.CTkEntry(
            add_row,
            placeholder_text="Market topic name",
        )
        self.name_entry.grid(row=0, column=0, sticky="ew", padx=8, pady=8)
        self.category_value = ctk.StringVar(value="Market")
        ctk.CTkOptionMenu(
            add_row,
            values=list(MarketTopic.CATEGORIES),
            variable=self.category_value,
            width=145,
        ).grid(row=0, column=1, padx=6, pady=8)
        self.keywords_entry = ctk.CTkEntry(
            add_row,
            placeholder_text="Keywords",
            width=190,
        )
        self.keywords_entry.grid(row=0, column=2, padx=6, pady=8)
        ctk.CTkButton(
            add_row,
            text="Add Topic",
            width=100,
            command=self.add_topic,
        ).grid(row=0, column=3, padx=8, pady=8)

        self.topic_list = ctk.CTkScrollableFrame(self)
        self.topic_list.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=15,
            pady=(6, 15),
        )

    def add_topic(self):
        name = self.name_entry.get().strip()
        if not name:
            return
        self.service.add_topic(
            name,
            category=self.category_value.get(),
            keywords=self.keywords_entry.get(),
        )
        self.name_entry.delete(0, "end")
        self.keywords_entry.delete(0, "end")
        self.refresh_topics()

    def refresh_topics(self):
        for widget in self.topic_list.winfo_children():
            widget.destroy()
        if not self.service.topics:
            ctk.CTkLabel(
                self.topic_list,
                text="No market topics yet.",
                anchor="w",
            ).pack(fill="x", padx=10, pady=12)
            return
        for topic in self.service.topics:
            summary = self.service.summary(topic.topic_id)
            row = ctk.CTkFrame(self.topic_list)
            row.pack(fill="x", padx=5, pady=5)
            row.grid_columnconfigure(0, weight=1)
            ctk.CTkLabel(
                row,
                text=(
                    f"{topic.name}\n"
                    f"{topic.category}   "
                    f"Latest: {summary['latest_direction']}   "
                    f"Observations: {summary['observations']}   "
                    f"Momentum: {summary['momentum']}"
                ),
                font=("Segoe UI", 13, "bold"),
                justify="left",
                anchor="w",
            ).grid(row=0, column=0, sticky="ew", padx=10, pady=9)
            ctk.CTkButton(
                row,
                text="Open Topic",
                width=100,
                command=lambda value=topic: self.open_topic(value),
            ).grid(row=0, column=1, padx=5, pady=9)
            ctk.CTkButton(
                row,
                text="Remove",
                width=75,
                command=lambda value=topic.topic_id: self.remove_topic(value),
            ).grid(row=0, column=2, padx=(5, 10), pady=9)

    def open_topic(self, topic):
        TrendTopicWindow(
            self,
            topic,
            self.service,
            on_change=self.refresh_topics,
        )

    def remove_topic(self, topic_id):
        self.service.remove_topic(topic_id)
        self.refresh_topics()
