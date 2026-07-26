"""Choose an accessible OpportunityLab text and control size."""

from __future__ import annotations

import customtkinter as ctk


class DisplaySettingsWindow(ctk.CTkToplevel):
    def __init__(self, master, service):
        super().__init__(master)
        self.service = service
        self.title("Text Size")
        self.geometry("540x270")
        self.minsize(480, 250)
        self.transient(master)
        self.grid_columnconfigure(0, weight=1)
        self.build_ui()

    def build_ui(self):
        ctk.CTkLabel(
            self,
            text="Text Size",
            font=("Segoe UI", 22, "bold"),
            anchor="w",
        ).grid(row=0, column=0, sticky="ew", padx=18, pady=(18, 8))
        ctk.CTkLabel(
            self,
            text=(
                "Increase text, buttons, menus, and form controls throughout "
                "OpportunityLab."
            ),
            justify="left",
            anchor="w",
            wraplength=490,
        ).grid(row=1, column=0, sticky="ew", padx=18, pady=8)
        self.selector = ctk.CTkSegmentedButton(
            self,
            values=list(self.service.LEVELS),
            command=self.change_size,
            height=44,
        )
        self.selector.grid(row=2, column=0, sticky="ew", padx=18, pady=12)
        self.selector.set(self.service.selected)
        self.message = ctk.CTkLabel(
            self,
            text=f"Current size: {self.service.selected}",
            anchor="w",
        )
        self.message.grid(row=3, column=0, sticky="ew", padx=18, pady=(8, 18))

    def change_size(self, name):
        try:
            scale = self.service.select(name)
            ctk.set_widget_scaling(scale)
        except (OSError, ValueError) as exc:
            self.message.configure(text=f"Could not change text size: {exc}")
            return
        self.message.configure(text=f"Current size: {name}")
