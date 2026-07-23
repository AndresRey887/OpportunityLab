"""Review likely duplicate opportunity families."""

from __future__ import annotations

import webbrowser

import customtkinter as ctk


class DuplicateClustersWindow(ctk.CTkToplevel):
    def __init__(self, master, service):
        super().__init__(master)
        self.service = service
        self.title("Duplicate Opportunity Clusters")
        self.geometry("900x740")
        self.minsize(720, 560)
        self.transient(master)
        self.build_ui()
        self.refresh_clusters()

    def build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        header = ctk.CTkFrame(self)
        header.grid(row=0, column=0, sticky="ew", padx=12, pady=12)
        header.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(
            header,
            text="Related Opportunity Families",
            font=("Segoe UI", 21, "bold"),
            anchor="w",
        ).grid(row=0, column=0, sticky="ew", padx=12, pady=12)
        ctk.CTkButton(
            header,
            text="Refresh",
            width=90,
            command=self.refresh_clusters,
        ).grid(row=0, column=1, padx=12, pady=12)

        self.cluster_list = ctk.CTkScrollableFrame(self)
        self.cluster_list.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=12,
            pady=(0, 8),
        )
        self.message = ctk.CTkLabel(self, text="", anchor="w")
        self.message.grid(row=2, column=0, sticky="ew", padx=18, pady=(0, 12))

    def refresh_clusters(self):
        for widget in self.cluster_list.winfo_children():
            widget.destroy()
        clusters = self.service.find_clusters(
            self.master.tracking_service.records
        )
        if not clusters:
            ctk.CTkLabel(
                self.cluster_list,
                text="No likely duplicate families found.",
                anchor="w",
            ).pack(fill="x", padx=12, pady=15)
            return
        for cluster in clusters:
            self._add_cluster(cluster)

    def _add_cluster(self, cluster):
        family = ctk.CTkFrame(self.cluster_list)
        family.pack(fill="x", padx=5, pady=7)
        family.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            family,
            text=(
                f"Primary: {cluster.primary.title}\n"
                f"{cluster.member_count} related discoveries   "
                f"Highest confidence: {cluster.highest_confidence}%"
            ),
            font=("Segoe UI", 14, "bold"),
            justify="left",
            anchor="w",
            wraplength=700,
        ).grid(row=0, column=0, sticky="ew", padx=12, pady=10)
        ctk.CTkButton(
            family,
            text="Open Primary",
            width=110,
            command=lambda: self.open_url(cluster.primary.url),
        ).grid(row=0, column=1, padx=12, pady=10)

        for row_number, match in enumerate(cluster.matches, start=1):
            row = ctk.CTkFrame(family)
            row.grid(
                row=row_number,
                column=0,
                columnspan=2,
                sticky="ew",
                padx=10,
                pady=(0, 7),
            )
            row.grid_columnconfigure(0, weight=1)
            ctk.CTkLabel(
                row,
                text=(
                    f"{match.record.title}\n"
                    f"Confidence: {match.confidence}%   "
                    f"Why: {', '.join(match.reasons)}"
                ),
                justify="left",
                anchor="w",
                wraplength=600,
            ).grid(row=0, column=0, sticky="ew", padx=10, pady=8)
            ctk.CTkButton(
                row,
                text="Open",
                width=70,
                command=lambda item=match.record: self.open_url(item.url),
            ).grid(row=0, column=1, padx=5, pady=8)
            ctk.CTkButton(
                row,
                text="Not Related",
                width=100,
                fg_color="#A36A2D",
                hover_color="#7F5223",
                command=lambda item=match.record, primary=cluster.primary: self.ignore_pair(
                    primary,
                    item,
                ),
            ).grid(row=0, column=2, padx=(5, 10), pady=8)

    def ignore_pair(self, first, second):
        self.service.ignore_pair(first, second)
        self.message.configure(text="Pair marked as not related.")
        self.refresh_clusters()

    @staticmethod
    def open_url(url):
        if url:
            webbrowser.open(url)
