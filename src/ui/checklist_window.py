"""Interactive checklist for one tracked opportunity."""

from __future__ import annotations

import webbrowser

import customtkinter as ctk


class ChecklistWindow(ctk.CTkToplevel):
    def __init__(self, master, workflow, service, opportunity_url=""):
        super().__init__(master)
        self.workflow = workflow
        self.service = service
        self.opportunity_url = opportunity_url

        self.title("Opportunity Checklist")
        self.geometry("680x680")
        self.minsize(560, 520)
        self.transient(master)
        self.build_ui()
        self.refresh_items()

    def build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(
            self,
            text=self.workflow.title,
            font=("Segoe UI", 20, "bold"),
            anchor="w",
            wraplength=600,
        ).grid(row=0, column=0, sticky="ew", padx=15, pady=(15, 5))

        header = ctk.CTkFrame(self)
        header.grid(row=1, column=0, sticky="ew", padx=15, pady=8)
        header.grid_columnconfigure(0, weight=1)

        self.progress_label = ctk.CTkLabel(header, text="", anchor="w")
        self.progress_label.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        ctk.CTkButton(
            header,
            text="Open Opportunity",
            width=130,
            command=self.open_opportunity,
        ).grid(row=0, column=1, padx=10, pady=10)

        self.item_list = ctk.CTkScrollableFrame(self)
        self.item_list.grid(row=2, column=0, sticky="nsew", padx=15, pady=8)

        add_row = ctk.CTkFrame(self)
        add_row.grid(row=3, column=0, sticky="ew", padx=15, pady=(8, 15))
        add_row.grid_columnconfigure(0, weight=1)

        self.new_item_entry = ctk.CTkEntry(
            add_row,
            placeholder_text="Add a custom action",
        )
        self.new_item_entry.grid(row=0, column=0, sticky="ew", padx=8, pady=8)
        self.new_item_entry.bind("<Return>", lambda event: self.add_item())

        ctk.CTkButton(
            add_row,
            text="Add Action",
            width=110,
            command=self.add_item,
        ).grid(row=0, column=1, padx=8, pady=8)

    def refresh_items(self):
        for widget in self.item_list.winfo_children():
            widget.destroy()

        total = len(self.workflow.items)
        self.progress_label.configure(
            text=(
                f"Progress: {self.workflow.completed_count}/{total} "
                f"({self.workflow.progress_percent}%)"
            )
        )

        for item in self.workflow.items:
            row = ctk.CTkFrame(self.item_list)
            row.pack(fill="x", padx=5, pady=4)
            row.grid_columnconfigure(0, weight=1)

            completed = ctk.BooleanVar(value=item.completed)
            ctk.CTkCheckBox(
                row,
                text=item.text,
                variable=completed,
                command=lambda action=item, value=completed: self.toggle_item(
                    action.item_id,
                    value.get(),
                ),
            ).grid(row=0, column=0, sticky="w", padx=10, pady=9)

            ctk.CTkButton(
                row,
                text="Remove",
                width=75,
                command=lambda action=item: self.remove_item(action.item_id),
            ).grid(row=0, column=1, padx=8, pady=6)

    def toggle_item(self, item_id, completed):
        self.service.set_completed(
            self.workflow.tracking_id,
            item_id,
            completed,
        )
        self.refresh_items()

    def add_item(self):
        text = self.new_item_entry.get().strip()
        if not text:
            return
        self.service.add_item(self.workflow.tracking_id, text)
        self.new_item_entry.delete(0, "end")
        self.refresh_items()

    def remove_item(self, item_id):
        self.service.remove_item(self.workflow.tracking_id, item_id)
        self.refresh_items()

    def open_opportunity(self):
        if self.opportunity_url:
            webbrowser.open(self.opportunity_url)
