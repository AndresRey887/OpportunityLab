"""Dashboard for reviewing OpportunityLab decision quality."""

from __future__ import annotations

import customtkinter as ctk
from tkinter import filedialog


class DecisionReviewWindow(ctk.CTkToplevel):
    def __init__(self, master, service, export_service):
        super().__init__(master)
        self.service = service
        self.export_service = export_service
        self.title("Decision Review")
        self.geometry("1040x780")
        self.minsize(820, 620)
        self.transient(master)
        self.build_ui()
        self.refresh_review()

    def build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        header = ctk.CTkFrame(self)
        header.grid(row=0, column=0, sticky="ew", padx=12, pady=12)
        header.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(
            header,
            text="Decision Review",
            font=("Segoe UI", 22, "bold"),
            anchor="w",
        ).grid(row=0, column=0, sticky="ew", padx=12, pady=12)
        ctk.CTkButton(
            header,
            text="Export Learning",
            width=120,
            command=self.export_learning,
        ).grid(row=0, column=1, padx=6, pady=12)
        ctk.CTkButton(
            header,
            text="Refresh",
            width=90,
            command=self.refresh_review,
        ).grid(row=0, column=2, padx=12, pady=12)

        self.summary_frame = ctk.CTkFrame(self)
        self.summary_frame.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=12,
            pady=(0, 8),
        )
        for column in range(5):
            self.summary_frame.grid_columnconfigure(column, weight=1)

        self.tabs = ctk.CTkTabview(self)
        self.tabs.grid(row=2, column=0, sticky="nsew", padx=12, pady=(0, 12))
        self.frames = {}
        for name in (
            "Strong Patterns",
            "Weak Patterns",
            "Evidence Gaps",
            "Lessons",
        ):
            tab = self.tabs.add(name)
            tab.grid_columnconfigure(0, weight=1)
            tab.grid_rowconfigure(0, weight=1)
            frame = ctk.CTkScrollableFrame(tab)
            frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
            self.frames[name] = frame

    def refresh_review(self):
        for widget in self.summary_frame.winfo_children():
            widget.destroy()
        summary = self.service.summary()
        metrics = (
            ("Tracked", summary["tracked"]),
            ("Outcomes", summary["decided"]),
            ("Success Rate", f"{summary['success_rate']}%"),
            ("Recommendation Accuracy", f"{summary['recommendation_accuracy']}%"),
            ("Duplicate Families", summary["duplicate_families"]),
        )
        for column, (label, value) in enumerate(metrics):
            card = ctk.CTkFrame(self.summary_frame)
            card.grid(row=0, column=column, sticky="nsew", padx=5, pady=8)
            ctk.CTkLabel(
                card,
                text=str(value),
                font=("Segoe UI", 20, "bold"),
            ).pack(pady=(9, 2))
            ctk.CTkLabel(card, text=label, wraplength=160).pack(pady=(0, 9))

        self._show_patterns(
            self.frames["Strong Patterns"],
            self.service.strong_patterns(),
            "No strong patterns yet.",
        )
        self._show_patterns(
            self.frames["Weak Patterns"],
            self.service.weak_patterns(),
            "No weak patterns identified.",
        )
        self._show_messages(
            self.frames["Evidence Gaps"],
            self.service.evidence_gaps(),
        )
        self._show_messages(
            self.frames["Lessons"],
            self.service.lessons() or ["No lessons recorded yet."],
        )

    @staticmethod
    def _clear(frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def _show_patterns(self, frame, patterns, empty_message):
        self._clear(frame)
        if not patterns:
            ctk.CTkLabel(frame, text=empty_message, anchor="w").pack(
                fill="x",
                padx=10,
                pady=12,
            )
            return
        for pattern in patterns:
            ctk.CTkLabel(
                frame,
                text=(
                    f"{pattern.category}: {pattern.label}\n"
                    f"Strength: {pattern.strength}   "
                    f"Tracked: {pattern.tracked_count}   "
                    f"Average score: {pattern.average_score}/100   "
                    f"Rating: {pattern.average_rating}/5   "
                    f"Success: {pattern.success_rate}%"
                ),
                font=("Segoe UI", 13, "bold"),
                justify="left",
                anchor="w",
            ).pack(fill="x", padx=10, pady=7)

    def _show_messages(self, frame, messages):
        self._clear(frame)
        for message in messages:
            ctk.CTkLabel(
                frame,
                text=f"• {message}",
                justify="left",
                anchor="w",
                wraplength=900,
            ).pack(fill="x", padx=12, pady=7)

    def export_learning(self):
        path = filedialog.asksaveasfilename(
            parent=self,
            title="Export Pathfinder Learning Data",
            defaultextension=".json",
            initialfile="OpportunityLab-Pathfinder-Learning.json",
            filetypes=[("JSON files", "*.json")],
        )
        if path:
            self.export_service.export(path)
