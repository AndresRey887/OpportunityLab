"""Display OpportunityLab production-readiness diagnostics."""

from __future__ import annotations

import customtkinter as ctk
from tkinter import filedialog


class SystemHealthWindow(ctk.CTkToplevel):
    COLOURS = {
        "Passed": "#2E7D32",
        "Warning": "#A36A2D",
        "Failed": "#A33A3A",
    }

    def __init__(self, master, service):
        super().__init__(master)
        self.service = service
        self.title("System Health")
        self.geometry("820x700")
        self.minsize(660, 520)
        self.transient(master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        header = ctk.CTkFrame(self)
        header.grid(row=0, column=0, sticky="ew", padx=12, pady=12)
        header.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(
            header,
            text="System Health",
            font=("Segoe UI", 22, "bold"),
            anchor="w",
        ).grid(row=0, column=0, sticky="ew", padx=12, pady=12)
        ctk.CTkButton(
            header,
            text="Run Checks",
            width=105,
            command=self.run_checks,
        ).grid(row=0, column=1, padx=(12, 4), pady=12)
        ctk.CTkButton(
            header,
            text="Export Report",
            width=115,
            command=self.export_report,
        ).grid(row=0, column=2, padx=(4, 12), pady=12)

        self.summary = ctk.CTkLabel(self, text="", anchor="w")
        self.summary.grid(row=1, column=0, sticky="ew", padx=18, pady=(0, 8))
        self.check_list = ctk.CTkScrollableFrame(self)
        self.check_list.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=12,
            pady=(0, 12),
        )
        self.run_checks()

    def run_checks(self):
        report = self.service.run()
        self.summary.configure(
            text=(
                f"Overall: {report.overall_status}   "
                f"Passed: {report.passed}   Warnings: {report.warnings}   "
                f"Failed: {report.failed}"
            )
        )
        for widget in self.check_list.winfo_children():
            widget.destroy()
        for check in report.checks:
            row = ctk.CTkFrame(self.check_list)
            row.pack(fill="x", padx=5, pady=4)
            row.grid_columnconfigure(1, weight=1)
            ctk.CTkLabel(
                row,
                text=check.status,
                width=80,
                text_color=self.COLOURS[check.status],
                font=("Segoe UI", 13, "bold"),
            ).grid(row=0, column=0, padx=10, pady=9)
            ctk.CTkLabel(
                row,
                text=f"{check.name}\n{check.message}",
                justify="left",
                anchor="w",
                wraplength=620,
            ).grid(row=0, column=1, sticky="ew", padx=8, pady=9)

    def export_report(self):
        path = filedialog.asksaveasfilename(
            parent=self,
            title="Export System Health Report",
            defaultextension=".json",
            initialfile="OpportunityLab-System-Health.json",
            filetypes=[("JSON report", "*.json")],
        )
        if not path:
            return
        try:
            exported = self.service.export_report(path)
        except OSError as exc:
            self.summary.configure(text=f"Export failed: {exc}")
            return
        self.summary.configure(text=f"Health report exported: {exported.name}")
