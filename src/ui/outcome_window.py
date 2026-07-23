"""Record the result and lessons from a tracked opportunity."""

from __future__ import annotations

from datetime import date

import customtkinter as ctk

from src.outcomes.outcome_record import OutcomeRecord


class OutcomeWindow(ctk.CTkToplevel):
    def __init__(self, master, tracked_record, service, on_saved=None):
        super().__init__(master)
        self.tracked_record = tracked_record
        self.service = service
        self.outcome = service.get_or_create(tracked_record)
        self.on_saved = on_saved

        self.title("Opportunity Outcome")
        self.geometry("700x650")
        self.minsize(580, 520)
        self.transient(master)
        self.build_ui()
        self.load_outcome()

    def build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(5, weight=1)

        ctk.CTkLabel(
            self,
            text=self.tracked_record.title,
            font=("Segoe UI", 20, "bold"),
            anchor="w",
            wraplength=640,
        ).grid(row=0, column=0, sticky="ew", padx=15, pady=(15, 8))

        details = ctk.CTkFrame(self)
        details.grid(row=1, column=0, sticky="ew", padx=15, pady=6)
        details.grid_columnconfigure((0, 1, 2), weight=1)

        self.result_value = ctk.StringVar(value="Undecided")
        ctk.CTkOptionMenu(
            details,
            values=list(OutcomeRecord.RESULTS),
            variable=self.result_value,
        ).grid(row=0, column=0, sticky="ew", padx=8, pady=8)

        self.date_entry = ctk.CTkEntry(
            details,
            placeholder_text="Outcome date",
        )
        self.date_entry.grid(row=0, column=1, sticky="ew", padx=8, pady=8)

        self.value_entry = ctk.CTkEntry(
            details,
            placeholder_text="Estimated value ($)",
        )
        self.value_entry.grid(row=0, column=2, sticky="ew", padx=8, pady=8)

        ctk.CTkLabel(
            self,
            text="Result notes",
            anchor="w",
            font=("Segoe UI", 13, "bold"),
        ).grid(row=2, column=0, sticky="ew", padx=18, pady=(8, 3))
        self.notes_text = ctk.CTkTextbox(self, height=130, wrap="word")
        self.notes_text.grid(row=3, column=0, sticky="ew", padx=15, pady=4)

        ctk.CTkLabel(
            self,
            text="Lessons learned",
            anchor="w",
            font=("Segoe UI", 13, "bold"),
        ).grid(row=4, column=0, sticky="ew", padx=18, pady=(8, 3))
        self.lessons_text = ctk.CTkTextbox(self, wrap="word")
        self.lessons_text.grid(row=5, column=0, sticky="nsew", padx=15, pady=4)

        footer = ctk.CTkFrame(self)
        footer.grid(row=6, column=0, sticky="ew", padx=15, pady=(8, 15))
        footer.grid_columnconfigure(0, weight=1)
        self.message = ctk.CTkLabel(footer, text="", anchor="w")
        self.message.grid(row=0, column=0, sticky="ew", padx=8, pady=8)
        ctk.CTkButton(
            footer,
            text="Save Outcome",
            command=self.save_outcome,
        ).grid(row=0, column=1, padx=8, pady=8)

    def load_outcome(self):
        self.result_value.set(self.outcome.result)
        self.date_entry.delete(0, "end")
        self.date_entry.insert(0, self.outcome.outcome_date)
        self.value_entry.delete(0, "end")
        if self.outcome.estimated_value:
            self.value_entry.insert(0, f"{self.outcome.estimated_value:g}")
        self.notes_text.delete("1.0", "end")
        self.notes_text.insert("1.0", self.outcome.result_notes)
        self.lessons_text.delete("1.0", "end")
        self.lessons_text.insert("1.0", self.outcome.lessons_learned)

    def save_outcome(self):
        outcome_date = self.date_entry.get().strip()
        if self.result_value.get() != "Undecided" and not outcome_date:
            outcome_date = date.today().isoformat()
            self.date_entry.insert(0, outcome_date)
        self.service.update(
            self.tracked_record.tracking_id,
            result=self.result_value.get(),
            outcome_date=outcome_date,
            estimated_value=self.value_entry.get(),
            result_notes=self.notes_text.get("1.0", "end"),
            lessons_learned=self.lessons_text.get("1.0", "end"),
        )
        self.message.configure(text="Outcome saved.")
        if self.on_saved is not None:
            self.on_saved()
