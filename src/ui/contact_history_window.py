"""Contact details and interaction history for one opportunity."""

from __future__ import annotations

import webbrowser
from datetime import date

import customtkinter as ctk

from src.contacts.interaction_entry import InteractionEntry


class ContactHistoryWindow(ctk.CTkToplevel):
    def __init__(self, master, record, service):
        super().__init__(master)
        self.record = record
        self.service = service
        self.contact = service.get_or_create_contact(record)

        self.title("Contacts and History")
        self.geometry("850x780")
        self.minsize(700, 620)
        self.transient(master)
        self.build_ui()
        self.load_contact()
        self.refresh_history()

    def build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        ctk.CTkLabel(
            self,
            text=self.record.title,
            font=("Segoe UI", 20, "bold"),
            anchor="w",
            wraplength=780,
        ).grid(row=0, column=0, sticky="ew", padx=15, pady=(15, 8))

        contact_frame = ctk.CTkFrame(self)
        contact_frame.grid(row=1, column=0, sticky="ew", padx=15, pady=6)
        contact_frame.grid_columnconfigure((0, 1), weight=1)

        self.name_entry = self._entry(contact_frame, "Contact name", 0, 0)
        self.organisation_entry = self._entry(contact_frame, "Organisation", 0, 1)
        self.email_entry = self._entry(contact_frame, "Email", 1, 0)
        self.phone_entry = self._entry(contact_frame, "Phone", 1, 1)
        self.website_entry = self._entry(contact_frame, "Website", 2, 0, 2)
        self.notes_entry = self._entry(contact_frame, "Contact notes", 3, 0, 2)

        ctk.CTkButton(
            contact_frame,
            text="Save Contact",
            command=self.save_contact,
        ).grid(row=4, column=0, sticky="w", padx=8, pady=8)
        ctk.CTkButton(
            contact_frame,
            text="Open Website",
            command=self.open_website,
        ).grid(row=4, column=1, sticky="e", padx=8, pady=8)

        add_frame = ctk.CTkFrame(self)
        add_frame.grid(row=2, column=0, sticky="ew", padx=15, pady=6)
        add_frame.grid_columnconfigure(2, weight=1)

        self.date_entry = ctk.CTkEntry(add_frame, width=120)
        self.date_entry.insert(0, date.today().isoformat())
        self.date_entry.grid(row=0, column=0, padx=8, pady=8)

        self.type_value = ctk.StringVar(value="Email")
        ctk.CTkOptionMenu(
            add_frame,
            values=list(InteractionEntry.TYPES),
            variable=self.type_value,
            width=120,
        ).grid(row=0, column=1, padx=8, pady=8)

        self.summary_entry = ctk.CTkEntry(
            add_frame,
            placeholder_text="What happened?",
        )
        self.summary_entry.grid(row=0, column=2, sticky="ew", padx=8, pady=8)
        self.summary_entry.bind("<Return>", lambda event: self.add_interaction())

        ctk.CTkButton(
            add_frame,
            text="Add History",
            width=110,
            command=self.add_interaction,
        ).grid(row=0, column=3, padx=8, pady=8)

        self.history_list = ctk.CTkScrollableFrame(self)
        self.history_list.grid(row=3, column=0, sticky="nsew", padx=15, pady=6)

        self.message = ctk.CTkLabel(self, text="", anchor="w")
        self.message.grid(row=4, column=0, sticky="ew", padx=18, pady=(3, 12))

    @staticmethod
    def _entry(parent, placeholder, row, column, columnspan=1):
        entry = ctk.CTkEntry(parent, placeholder_text=placeholder)
        entry.grid(
            row=row,
            column=column,
            columnspan=columnspan,
            sticky="ew",
            padx=8,
            pady=6,
        )
        return entry

    def load_contact(self):
        values = (
            (self.name_entry, self.contact.contact_name),
            (self.organisation_entry, self.contact.organisation),
            (self.email_entry, self.contact.email),
            (self.phone_entry, self.contact.phone),
            (self.website_entry, self.contact.website),
            (self.notes_entry, self.contact.notes),
        )
        for entry, value in values:
            entry.delete(0, "end")
            entry.insert(0, value)

    def save_contact(self):
        self.service.update_contact(
            self.record.tracking_id,
            contact_name=self.name_entry.get(),
            organisation=self.organisation_entry.get(),
            email=self.email_entry.get(),
            phone=self.phone_entry.get(),
            website=self.website_entry.get(),
            notes=self.notes_entry.get(),
        )
        self.message.configure(text="Contact saved.")

    def add_interaction(self):
        summary = self.summary_entry.get().strip()
        if not summary:
            self.message.configure(text="Enter what happened.")
            return
        self.service.add_interaction(
            self.record.tracking_id,
            self.type_value.get(),
            summary,
            self.date_entry.get().strip() or date.today().isoformat(),
        )
        self.summary_entry.delete(0, "end")
        self.message.configure(text="History entry added.")
        self.refresh_history()

    def refresh_history(self):
        for widget in self.history_list.winfo_children():
            widget.destroy()
        history = self.service.history(self.record.tracking_id)
        if not history:
            ctk.CTkLabel(
                self.history_list,
                text="No interaction history yet.",
                anchor="w",
            ).pack(fill="x", padx=10, pady=12)
            return
        for entry in history:
            row = ctk.CTkFrame(self.history_list)
            row.pack(fill="x", padx=5, pady=4)
            row.grid_columnconfigure(0, weight=1)
            ctk.CTkLabel(
                row,
                text=(
                    f"{entry.interaction_date}  |  {entry.interaction_type}\n"
                    f"{entry.summary}"
                ),
                justify="left",
                anchor="w",
                wraplength=650,
            ).grid(row=0, column=0, sticky="ew", padx=10, pady=8)
            ctk.CTkButton(
                row,
                text="Remove",
                width=75,
                command=lambda item=entry: self.remove_interaction(item.entry_id),
            ).grid(row=0, column=1, padx=8, pady=8)

    def remove_interaction(self, entry_id):
        self.service.remove_interaction(entry_id)
        self.message.configure(text="History entry removed.")
        self.refresh_history()

    def open_website(self):
        url = self.website_entry.get().strip() or self.record.url
        if url:
            webbrowser.open(url)
