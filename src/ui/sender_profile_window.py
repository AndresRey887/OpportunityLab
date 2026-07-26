"""Create and edit sender identity profiles."""

from __future__ import annotations

import customtkinter as ctk


class SenderProfileWindow(ctk.CTkToplevel):
    FIELDS = (
        ("name", "Profile name"),
        ("sender_name", "Sender name"),
        ("role", "Role or title"),
        ("organisation", "Organisation"),
        ("email", "Email address"),
        ("website", "Website"),
        ("organisation_description", "Organisation description"),
        ("charity_information", "Charity information"),
        ("signature", "Custom signature (optional)"),
        ("tone", "Writing tone"),
    )

    def __init__(self, master, service, on_saved=None):
        super().__init__(master)
        self.service = service
        self.on_saved = on_saved
        self.entries = {}
        self.title("Sender Profiles")
        self.geometry("680x760")
        self.minsize(560, 620)
        self.transient(master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.build_ui()
        self.refresh_profiles()

    def build_ui(self):
        ctk.CTkLabel(
            self,
            text="Sender Profiles",
            font=("Segoe UI", 22, "bold"),
            anchor="w",
        ).grid(row=0, column=0, sticky="ew", padx=18, pady=(18, 8))

        selector_row = ctk.CTkFrame(self)
        selector_row.grid(row=1, column=0, sticky="ew", padx=18, pady=8)
        selector_row.grid_columnconfigure(0, weight=1)
        self.profile_value = ctk.StringVar()
        self.profile_menu = ctk.CTkOptionMenu(
            selector_row,
            variable=self.profile_value,
            command=self.select_profile,
        )
        self.profile_menu.grid(row=0, column=0, sticky="ew", padx=8, pady=8)
        ctk.CTkButton(
            selector_row,
            text="New",
            width=80,
            command=self.new_profile,
        ).grid(row=0, column=1, padx=5, pady=8)
        ctk.CTkButton(
            selector_row,
            text="Delete",
            width=80,
            fg_color="#A33A3A",
            hover_color="#7F2D2D",
            command=self.delete_profile,
        ).grid(row=0, column=2, padx=8, pady=8)

        form = ctk.CTkScrollableFrame(self)
        form.grid(row=2, column=0, sticky="nsew", padx=18, pady=8)
        form.grid_columnconfigure(0, weight=1)
        for row, (name, placeholder) in enumerate(self.FIELDS):
            entry = ctk.CTkEntry(form, placeholder_text=placeholder, height=38)
            entry.grid(row=row, column=0, sticky="ew", padx=8, pady=6)
            self.entries[name] = entry

        action_row = ctk.CTkFrame(self)
        action_row.grid(row=3, column=0, sticky="ew", padx=18, pady=(8, 18))
        action_row.grid_columnconfigure(0, weight=1)
        self.message = ctk.CTkLabel(action_row, text="", anchor="w")
        self.message.grid(row=0, column=0, sticky="ew", padx=8, pady=8)
        ctk.CTkButton(
            action_row,
            text="Save Profile",
            width=120,
            command=self.save_profile,
        ).grid(row=0, column=1, padx=8, pady=8)

    def refresh_profiles(self):
        names = self.service.names()
        self.profile_menu.configure(values=names)
        active = self.service.active_profile
        self.profile_value.set(active.name)
        self.load_profile(active)
        if callable(self.on_saved):
            self.on_saved()

    def select_profile(self, name):
        profile = self.service.set_active_by_name(name)
        self.load_profile(profile)
        self.message.configure(text=f"{name} is now active.")
        if callable(self.on_saved):
            self.on_saved()

    def load_profile(self, profile):
        for name, entry in self.entries.items():
            entry.delete(0, "end")
            entry.insert(0, getattr(profile, name))

    def new_profile(self):
        profile = self.service.create()
        self.refresh_profiles()
        self.profile_value.set(profile.name)
        self.load_profile(profile)
        self.message.configure(text="New profile created. Add details and save.")

    def save_profile(self):
        profile = self.service.active_profile
        values = {
            name: entry.get()
            for name, entry in self.entries.items()
        }
        try:
            self.service.update(profile.profile_id, **values)
        except (OSError, ValueError) as exc:
            self.message.configure(text=f"Could not save profile: {exc}")
            return
        self.refresh_profiles()
        self.message.configure(text="Profile saved and selected.")

    def delete_profile(self):
        profile = self.service.active_profile
        try:
            self.service.delete(profile.profile_id)
        except (OSError, ValueError) as exc:
            self.message.configure(text=f"Could not delete profile: {exc}")
            return
        self.refresh_profiles()
        self.message.configure(text="Profile deleted.")
