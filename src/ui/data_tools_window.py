"""Backup and restore controls for OpportunityLab data."""

from __future__ import annotations

from datetime import date
from tkinter import filedialog, messagebox

import customtkinter as ctk

from src.backups.backup_service import BackupError


class DataToolsWindow(ctk.CTkToplevel):
    def __init__(self, master, service):
        super().__init__(master)
        self.service = service
        self.title("Data Backup and Restore")
        self.geometry("560x330")
        self.minsize(500, 300)
        self.transient(master)
        self.build_ui()

    def build_ui(self):
        self.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self,
            text="Data Backup and Restore",
            font=("Segoe UI", 21, "bold"),
            anchor="w",
        ).grid(row=0, column=0, sticky="ew", padx=18, pady=(18, 8))

        ctk.CTkLabel(
            self,
            text=(
                "Back up tracked opportunities, schedules, checklists, "
                "drafts, contacts, history, and other saved app data."
            ),
            justify="left",
            anchor="w",
            wraplength=500,
        ).grid(row=1, column=0, sticky="ew", padx=18, pady=8)

        ctk.CTkButton(
            self,
            text="Create Backup",
            height=42,
            command=self.create_backup,
        ).grid(row=2, column=0, sticky="ew", padx=18, pady=8)

        ctk.CTkButton(
            self,
            text="Restore Backup",
            height=42,
            fg_color="#A36A2D",
            hover_color="#7F5223",
            command=self.restore_backup,
        ).grid(row=3, column=0, sticky="ew", padx=18, pady=8)

        self.message = ctk.CTkLabel(
            self,
            text="",
            justify="left",
            anchor="w",
            wraplength=500,
        )
        self.message.grid(row=4, column=0, sticky="ew", padx=18, pady=(8, 18))

    def create_backup(self):
        path = filedialog.asksaveasfilename(
            parent=self,
            title="Create OpportunityLab Backup",
            defaultextension=".zip",
            initialfile=f"OpportunityLab-Backup-{date.today().isoformat()}.zip",
            filetypes=[("ZIP backup", "*.zip")],
        )
        if not path:
            return
        try:
            self.service.create_backup(path)
        except OSError as exc:
            self.message.configure(text=f"Backup failed: {exc}")
            return
        self.message.configure(text="Backup created successfully.")

    def restore_backup(self):
        path = filedialog.askopenfilename(
            parent=self,
            title="Select OpportunityLab Backup",
            filetypes=[("ZIP backup", "*.zip")],
        )
        if not path:
            return
        if not messagebox.askyesno(
            "Restore Backup",
            (
                "Restore saved data from this backup?\n\n"
                "Current files with matching names will be replaced."
            ),
            parent=self,
        ):
            return
        try:
            restored = self.service.restore_backup(path)
        except (BackupError, OSError) as exc:
            self.message.configure(text=f"Restore failed: {exc}")
            return
        self.message.configure(
            text=(
                f"Restored {len(restored)} data files. "
                "Restart OpportunityLab to load them."
            )
        )
