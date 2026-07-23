"""Display an explainable recommendation for one opportunity."""

from __future__ import annotations

import customtkinter as ctk


class RecommendationWindow(ctk.CTkToplevel):
    def __init__(
        self,
        master,
        opportunity,
        recommendation,
        feedback_service,
    ):
        super().__init__(master)
        self.opportunity = opportunity
        self.feedback_service = feedback_service
        self.title("Opportunity Recommendation")
        self.geometry("720x650")
        self.minsize(600, 520)
        self.transient(master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        ctk.CTkLabel(
            self,
            text=opportunity.title,
            font=("Segoe UI", 20, "bold"),
            anchor="w",
            wraplength=650,
        ).grid(row=0, column=0, sticky="ew", padx=15, pady=(15, 8))

        score_frame = ctk.CTkFrame(self)
        score_frame.grid(row=1, column=0, sticky="ew", padx=15, pady=6)
        score_frame.grid_columnconfigure((0, 1, 2), weight=1)
        self._metric(score_frame, 0, recommendation.label, "Recommendation")
        self._metric(
            score_frame,
            1,
            f"{recommendation.match_score}/100",
            "Match score",
        )
        self._metric(
            score_frame,
            2,
            f"{recommendation.confidence}%",
            "Confidence",
        )

        ctk.CTkLabel(
            self,
            text=(
                f"Based on {recommendation.evidence_count} tracked and "
                f"completed evidence points."
            ),
            anchor="w",
        ).grid(row=2, column=0, sticky="ew", padx=18, pady=6)

        body = ctk.CTkScrollableFrame(self)
        body.grid(row=3, column=0, sticky="nsew", padx=15, pady=(6, 15))
        self._section(body, "Why OpportunityLab recommends this", recommendation.reasons)
        self._section(
            body,
            "What to keep in mind",
            recommendation.cautions or ("No specific cautions identified.",),
        )

        feedback = ctk.CTkFrame(self)
        feedback.grid(row=4, column=0, sticky="ew", padx=15, pady=(0, 15))
        feedback.grid_columnconfigure(0, weight=1)
        self.feedback_note = ctk.CTkEntry(
            feedback,
            placeholder_text="Optional feedback note",
        )
        self.feedback_note.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=8,
            pady=8,
        )
        ctk.CTkButton(
            feedback,
            text="Helpful",
            width=90,
            command=lambda: self.save_feedback(True),
        ).grid(row=0, column=1, padx=5, pady=8)
        ctk.CTkButton(
            feedback,
            text="Not Helpful",
            width=100,
            fg_color="#A36A2D",
            hover_color="#7F5223",
            command=lambda: self.save_feedback(False),
        ).grid(row=0, column=2, padx=5, pady=8)
        self.feedback_message = ctk.CTkLabel(
            feedback,
            text="",
            anchor="w",
        )
        self.feedback_message.grid(
            row=1,
            column=0,
            columnspan=3,
            sticky="ew",
            padx=8,
            pady=(0, 8),
        )

    @staticmethod
    def _metric(parent, column, value, label):
        frame = ctk.CTkFrame(parent)
        frame.grid(row=0, column=column, sticky="nsew", padx=5, pady=8)
        ctk.CTkLabel(
            frame,
            text=value,
            font=("Segoe UI", 18, "bold"),
            wraplength=190,
        ).pack(pady=(10, 2))
        ctk.CTkLabel(frame, text=label).pack(pady=(0, 10))

    @staticmethod
    def _section(parent, heading, items):
        ctk.CTkLabel(
            parent,
            text=heading,
            font=("Segoe UI", 15, "bold"),
            anchor="w",
        ).pack(fill="x", padx=10, pady=(12, 5))
        for item in items:
            ctk.CTkLabel(
                parent,
                text=f"• {item}",
                justify="left",
                anchor="w",
                wraplength=620,
            ).pack(fill="x", padx=15, pady=4)

    def save_feedback(self, helpful):
        self.feedback_service.record(
            self.opportunity,
            helpful,
            self.feedback_note.get(),
        )
        self.feedback_note.delete(0, "end")
        self.feedback_message.configure(
            text=(
                "Helpful feedback saved."
                if helpful
                else "Not Helpful feedback saved."
            )
        )
