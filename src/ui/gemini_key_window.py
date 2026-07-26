"""Manual primary/alternate Gemini API key selector."""

from __future__ import annotations

import customtkinter as ctk

from src.ai.gemini_key_service import GeminiKeyService


class GeminiKeyWindow(ctk.CTkToplevel):
    def __init__(self, master, ai_controller):
        super().__init__(master)
        self.ai_controller = ai_controller
        self.title("Gemini API Key")
        self.geometry("520x300")
        self.minsize(480, 280)
        self.transient(master)
        self.grid_columnconfigure(0, weight=1)
        self.build_ui()
        self.refresh()

    def build_ui(self):
        ctk.CTkLabel(
            self,
            text="Gemini API Key",
            font=("Segoe UI", 21, "bold"),
            anchor="w",
        ).grid(row=0, column=0, sticky="ew", padx=18, pady=(18, 8))
        ctk.CTkLabel(
            self,
            text=(
                "Choose which configured Gemini key OpportunityLab uses. "
                "Key values are never displayed."
            ),
            justify="left",
            anchor="w",
            wraplength=470,
        ).grid(row=1, column=0, sticky="ew", padx=18, pady=8)
        self.selector = ctk.CTkSegmentedButton(
            self,
            values=list(GeminiKeyService.OPTIONS),
            command=self.change_selection,
            height=42,
        )
        self.selector.grid(row=2, column=0, sticky="ew", padx=18, pady=12)
        self.status_label = ctk.CTkLabel(
            self,
            text="",
            justify="left",
            anchor="w",
        )
        self.status_label.grid(row=3, column=0, sticky="ew", padx=18, pady=8)
        self.message = ctk.CTkLabel(
            self,
            text="",
            justify="left",
            anchor="w",
            wraplength=470,
        )
        self.message.grid(row=4, column=0, sticky="ew", padx=18, pady=(8, 18))

    def refresh(self):
        status = self.ai_controller.get_gemini_key_status()
        self.selector.set(status["selected"])
        primary = "Configured" if status["primary_configured"] else "Missing"
        alternate = (
            "Configured" if status["alternate_configured"] else "Missing"
        )
        self.status_label.configure(
            text=f"Primary: {primary}\nAlternate: {alternate}"
        )

    def change_selection(self, name):
        try:
            status = self.ai_controller.select_gemini_key(name)
        except (OSError, ValueError) as exc:
            self.message.configure(text=f"Could not switch key: {exc}")
            return
        if not self.ai_controller.gemini_key_service.is_configured(name):
            self.message.configure(
                text=f"{name} selected, but that key is not configured."
            )
        else:
            self.message.configure(text=f"{name} Gemini key is now active.")
        self.selector.set(status["selected"])
        self.refresh()
