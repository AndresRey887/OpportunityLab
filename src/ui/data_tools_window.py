"""Backup and restore controls for OpportunityLab data."""

from __future__ import annotations

from datetime import date
from tkinter import filedialog, messagebox

import customtkinter as ctk

from src.backups.backup_service import BackupError
from src.ui.system_health_window import SystemHealthWindow
from src.ui.gemini_key_window import GeminiKeyWindow
from src.ui.display_settings_window import DisplaySettingsWindow


class DataToolsWindow(ctk.CTkToplevel):
    def __init__(
        self,
        master,
        service,
        health_service,
        ai_controller,
        display_settings_service,
    ):
        super().__init__(master)
        self.service = service
        self.health_service = health_service
        self.ai_controller = ai_controller
        self.display_settings_service = display_settings_service
        self.system_health_window = None
        self.gemini_key_window = None
        self.display_settings_window = None
        self.title("Data Backup and Restore")
        self.geometry("560x540")
        self.minsize(500, 500)
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

        ctk.CTkButton(
            self,
            text="System Health",
            height=42,
            command=self.open_system_health,
        ).grid(row=4, column=0, sticky="ew", padx=18, pady=8)

        ctk.CTkButton(
            self,
            text="Gemini API Key",
            height=42,
            command=self.open_gemini_key,
        ).grid(row=5, column=0, sticky="ew", padx=18, pady=8)

        ctk.CTkButton(
            self,
            text="Text Size",
            height=42,
            command=self.open_display_settings,
        ).grid(row=6, column=0, sticky="ew", padx=18, pady=8)

        self.message = ctk.CTkLabel(
            self,
            text="",
            justify="left",
            anchor="w",
            wraplength=500,
        )
        self.message.grid(row=7, column=0, sticky="ew", padx=18, pady=(8, 18))

    def open_display_settings(self):
        if self.display_settings_window is not None:
            try:
                if self.display_settings_window.winfo_exists():
                    self.display_settings_window.focus()
                    return
            except Exception:
                pass
        self.display_settings_window = DisplaySettingsWindow(
            self,
            self.display_settings_service,
        )

    def open_gemini_key(self):
        if self.gemini_key_window is not None:
            try:
                if self.gemini_key_window.winfo_exists():
                    self.gemini_key_window.focus()
                    return
            except Exception:
                pass
        self.gemini_key_window = GeminiKeyWindow(
            self,
            self.ai_controller,
        )

    def open_system_health(self):
        if self.system_health_window is not None:
            try:
                if self.system_health_window.winfo_exists():
                    self.system_health_window.focus()
                    return
            except Exception:
                pass
        self.system_health_window = SystemHealthWindow(
            self,
            self.health_service,
        )

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
