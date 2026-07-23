"""Review what OpportunityLab has learned from tracked results."""

from __future__ import annotations

import customtkinter as ctk


class SearchMemoryWindow(ctk.CTkToplevel):
    def __init__(self, master, service):
        super().__init__(master)
        self.service = service
        self.title("Search Memory")
        self.geometry("980x760")
        self.minsize(780, 600)
        self.transient(master)
        self.build_ui()
        self.refresh_memory()

    def build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        header = ctk.CTkFrame(self)
        header.grid(row=0, column=0, sticky="ew", padx=12, pady=12)
        header.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(
            header,
            text="Search Memory",
            font=("Segoe UI", 22, "bold"),
            anchor="w",
        ).grid(row=0, column=0, sticky="ew", padx=12, pady=12)
        ctk.CTkButton(
            header,
            text="Refresh",
            width=90,
            command=self.refresh_memory,
        ).grid(row=0, column=1, padx=12, pady=12)

        self.summary_label = ctk.CTkLabel(
            self,
            text="",
            anchor="w",
            justify="left",
        )
        self.summary_label.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=18,
            pady=(0, 8),
        )

        self.tabs = ctk.CTkTabview(self)
        self.tabs.grid(row=2, column=0, sticky="nsew", padx=12, pady=(0, 12))
        self.profile_frames = {}
        for name in ("Sources", "Keywords", "Opportunity Types"):
            tab = self.tabs.add(name)
            tab.grid_columnconfigure(0, weight=1)
            tab.grid_rowconfigure(0, weight=1)
            frame = ctk.CTkScrollableFrame(tab)
            frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
            self.profile_frames[name] = frame

    def refresh_memory(self):
        summary = self.service.summary()
        self.summary_label.configure(
            text=(
                f"Tracked results learned from: {summary['tracked']}   "
                f"Best source: {summary['top_source']}   "
                f"Best keyword: {summary['top_keyword']}   "
                f"Best type: {summary['top_type']}"
            )
        )
        groups = {
            "Sources": self.service.source_profiles(),
            "Keywords": self.service.keyword_profiles(),
            "Opportunity Types": self.service.opportunity_type_profiles(),
        }
        for name, profiles in groups.items():
            frame = self.profile_frames[name]
            for widget in frame.winfo_children():
                widget.destroy()
            if not profiles:
                ctk.CTkLabel(
                    frame,
                    text="Track and rate more opportunities to build this profile.",
                    anchor="w",
                ).pack(fill="x", padx=10, pady=12)
                continue
            for profile in profiles:
                self._add_profile(frame, profile, name == "Keywords")

    def _add_profile(self, parent, profile, searchable):
        row = ctk.CTkFrame(parent)
        row.pack(fill="x", padx=5, pady=5)
        row.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(
            row,
            text=(
                f"{profile.label}\n"
                f"Tracked: {profile.tracked_count}   "
                f"Average score: {profile.average_score}/100   "
                f"Average rating: {profile.average_rating}/5   "
                f"Success: {profile.success_count}/{profile.decided_count} "
                f"({profile.success_rate}%)   "
                f"Strength: {profile.strength}"
            ),
            justify="left",
            anchor="w",
            font=("Segoe UI", 13, "bold"),
        ).grid(row=0, column=0, sticky="ew", padx=10, pady=9)
        if searchable:
            ctk.CTkButton(
                row,
                text="Use Search",
                width=95,
                command=lambda value=profile.label: self.use_search(value),
            ).grid(row=0, column=1, padx=10, pady=9)

    def use_search(self, query):
        self.master.search_box.delete(0, "end")
        self.master.search_box.insert(0, query)
        self.master.search_box.focus()
        self.destroy()
