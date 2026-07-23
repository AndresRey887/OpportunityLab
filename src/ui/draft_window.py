"""Opportunity-specific response draft workspace."""

from __future__ import annotations

import webbrowser

import customtkinter as ctk


class DraftWindow(ctk.CTkToplevel):
    def __init__(self, master, record, service):
        super().__init__(master)
        self.record = record
        self.service = service
        self.draft = service.get_or_create_draft(record)

        self.title("Response Draft")
        self.geometry("780x720")
        self.minsize(620, 560)
        self.transient(master)
        self.build_ui()
        self.load_draft()

    def build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        ctk.CTkLabel(
            self,
            text=self.record.title,
            font=("Segoe UI", 20, "bold"),
            anchor="w",
            wraplength=710,
        ).grid(row=0, column=0, sticky="ew", padx=15, pady=(15, 8))

        template_row = ctk.CTkFrame(self)
        template_row.grid(row=1, column=0, sticky="ew", padx=15, pady=5)
        template_row.grid_columnconfigure(0, weight=1)

        template_names = self.service.template_names()
        self.template_value = ctk.StringVar(
            value=template_names[0] if template_names else ""
        )
        self.template_menu = ctk.CTkOptionMenu(
            template_row,
            values=template_names or [""],
            variable=self.template_value,
        )
        self.template_menu.grid(row=0, column=0, sticky="ew", padx=8, pady=8)

        ctk.CTkButton(
            template_row,
            text="Apply Template",
            width=120,
            command=self.apply_template,
        ).grid(row=0, column=1, padx=8, pady=8)

        self.subject_entry = ctk.CTkEntry(
            self,
            placeholder_text="Subject",
        )
        self.subject_entry.grid(row=2, column=0, sticky="ew", padx=15, pady=8)

        self.body_text = ctk.CTkTextbox(self, wrap="word")
        self.body_text.grid(row=3, column=0, sticky="nsew", padx=15, pady=8)

        action_row = ctk.CTkFrame(self)
        action_row.grid(row=4, column=0, sticky="ew", padx=15, pady=(8, 5))
        action_row.grid_columnconfigure(0, weight=1)

        self.message = ctk.CTkLabel(action_row, text="", anchor="w")
        self.message.grid(row=0, column=0, sticky="ew", padx=8, pady=8)

        ctk.CTkButton(
            action_row,
            text="Open Opportunity",
            width=130,
            command=self.open_opportunity,
        ).grid(row=0, column=1, padx=5, pady=8)

        ctk.CTkButton(
            action_row,
            text="Copy Draft",
            width=105,
            command=self.copy_draft,
        ).grid(row=0, column=2, padx=5, pady=8)

        ctk.CTkButton(
            action_row,
            text="Save Draft",
            width=105,
            command=self.save_draft,
        ).grid(row=0, column=3, padx=8, pady=8)

        save_template = ctk.CTkFrame(self)
        save_template.grid(row=5, column=0, sticky="ew", padx=15, pady=(5, 15))
        save_template.grid_columnconfigure(0, weight=1)

        self.template_name_entry = ctk.CTkEntry(
            save_template,
            placeholder_text="Name this as a reusable template",
        )
        self.template_name_entry.grid(row=0, column=0, sticky="ew", padx=8, pady=8)
        ctk.CTkButton(
            save_template,
            text="Save Template",
            width=120,
            command=self.save_template,
        ).grid(row=0, column=1, padx=8, pady=8)

    def load_draft(self):
        self.subject_entry.delete(0, "end")
        self.subject_entry.insert(0, self.draft.subject)
        self.body_text.delete("1.0", "end")
        self.body_text.insert("1.0", self.draft.body)

    def apply_template(self):
        template = self.service.get_template_by_name(self.template_value.get())
        self.service.apply_template(self.draft, template, self.record)
        self.load_draft()
        self.message.configure(text="Template applied and draft saved.")

    def save_draft(self):
        self.service.save_draft(
            self.record.tracking_id,
            subject=self.subject_entry.get(),
            body=self.body_text.get("1.0", "end"),
        )
        self.message.configure(text="Draft saved.")

    def copy_draft(self):
        self.save_draft()
        text = f"{self.subject_entry.get().strip()}\n\n{self.body_text.get('1.0', 'end').strip()}"
        self.clipboard_clear()
        self.clipboard_append(text)
        self.message.configure(text="Draft copied.")

    def save_template(self):
        name = self.template_name_entry.get().strip()
        if not name:
            self.message.configure(text="Enter a template name.")
            return
        template = self.service.add_template(
            name,
            self.subject_entry.get(),
            self.body_text.get("1.0", "end"),
        )
        names = self.service.template_names()
        self.template_menu.configure(values=names)
        self.template_value.set(template.name)
        self.template_name_entry.delete(0, "end")
        self.message.configure(text="Reusable template saved.")

    def open_opportunity(self):
        if self.record.url:
            webbrowser.open(self.record.url)
