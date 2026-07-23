"""Monitor product launches and upcoming dates."""

from __future__ import annotations

import webbrowser

import customtkinter as ctk

from src.launches.product_launch import ProductLaunch


class ProductLaunchesWindow(ctk.CTkToplevel):
    def __init__(self, master, service, company_service):
        super().__init__(master)
        self.service = service
        self.company_service = company_service
        self.company_names = {}
        self.stage_filter = ctk.StringVar(value="All")
        self.title("Product Launches")
        self.geometry("1000x780")
        self.minsize(800, 620)
        self.transient(master)
        self.build_ui()
        self.refresh_companies()
        self.refresh_launches()

    def build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)
        header = ctk.CTkFrame(self)
        header.grid(row=0, column=0, sticky="ew", padx=12, pady=12)
        header.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(header, text="Product Launches", font=("Segoe UI", 22, "bold"), anchor="w").grid(row=0, column=0, sticky="ew", padx=12, pady=12)
        ctk.CTkOptionMenu(header, values=["All", *ProductLaunch.STAGES], variable=self.stage_filter, command=lambda value: self.refresh_launches(), width=140).grid(row=0, column=1, padx=12, pady=12)
        self.summary_label = ctk.CTkLabel(header, text="", anchor="w")
        self.summary_label.grid(row=1, column=0, columnspan=2, sticky="ew", padx=12, pady=(0, 10))

        form = ctk.CTkFrame(self)
        form.grid(row=1, column=0, sticky="ew", padx=12, pady=6)
        form.grid_columnconfigure((0, 1), weight=1)
        self.name_entry = self._entry(form, "Product or launch name", 0, 0, 2)
        self.company_value = ctk.StringVar(value="No company")
        self.company_menu = ctk.CTkOptionMenu(form, values=["No company"], variable=self.company_value)
        self.company_menu.grid(row=1, column=0, sticky="ew", padx=8, pady=5)
        self.stage_value = ctk.StringVar(value="Announced")
        ctk.CTkOptionMenu(form, values=list(ProductLaunch.STAGES), variable=self.stage_value).grid(row=1, column=1, sticky="ew", padx=8, pady=5)
        self.date_entry = self._entry(form, "Launch date, for example 2026-09-15", 2, 0)
        self.category_entry = self._entry(form, "Product category", 2, 1)
        self.url_entry = self._entry(form, "Source URL", 3, 0)
        self.notes_entry = self._entry(form, "Launch notes", 3, 1)
        ctk.CTkButton(form, text="Add Launch", command=self.add_launch).grid(row=4, column=0, columnspan=2, sticky="ew", padx=8, pady=8)

        self.message = ctk.CTkLabel(self, text="", anchor="w")
        self.message.grid(row=2, column=0, sticky="ew", padx=18, pady=4)
        self.launch_list = ctk.CTkScrollableFrame(self)
        self.launch_list.grid(row=3, column=0, sticky="nsew", padx=12, pady=(4, 12))

    @staticmethod
    def _entry(parent, placeholder, row, column, columnspan=1):
        entry = ctk.CTkEntry(parent, placeholder_text=placeholder)
        entry.grid(row=row, column=column, columnspan=columnspan, sticky="ew", padx=8, pady=5)
        return entry

    def refresh_companies(self):
        self.company_names = {"No company": None}
        self.company_names.update({profile.name: profile for profile in self.company_service.profiles})
        self.company_menu.configure(values=list(self.company_names))
        self.company_value.set("No company")

    def add_launch(self):
        name = self.name_entry.get().strip()
        if not name:
            self.message.configure(text="Enter a product or launch name.")
            return
        company = self.company_names.get(self.company_value.get())
        self.service.add(
            product_name=name,
            company_id=company.company_id if company else "",
            company_name=company.name if company else "",
            stage=self.stage_value.get(),
            launch_date=self.date_entry.get().strip(),
            category=self.category_entry.get(),
            source_url=self.url_entry.get(),
            notes=self.notes_entry.get(),
        )
        for entry in (self.name_entry, self.date_entry, self.category_entry, self.url_entry, self.notes_entry):
            entry.delete(0, "end")
        self.message.configure(text="Product launch saved.")
        self.refresh_launches()

    def refresh_launches(self):
        for widget in self.launch_list.winfo_children():
            widget.destroy()
        summary = self.service.summary()
        self.summary_label.configure(text=f"Launches: {summary['total']}   Upcoming 30 days: {summary['upcoming_30']}   Overdue: {summary['overdue']}   Released: {summary['released']}")
        for item in self.service.all(self.stage_filter.get()):
            row = ctk.CTkFrame(self.launch_list)
            row.pack(fill="x", padx=5, pady=5)
            row.grid_columnconfigure(0, weight=1)
            stage_value = ctk.StringVar(value=item.stage)
            ctk.CTkLabel(row, text=f"{item.product_name}\n{item.company_name or 'No company'}   Date: {item.launch_date or 'Not set'}   Category: {item.category or 'Not set'}", font=("Segoe UI", 13, "bold"), justify="left", anchor="w").grid(row=0, column=0, sticky="ew", padx=10, pady=8)
            ctk.CTkOptionMenu(row, values=list(ProductLaunch.STAGES), variable=stage_value, command=lambda value, launch=item: self.change_stage(launch.launch_id, value), width=120).grid(row=0, column=1, padx=5, pady=8)
            ctk.CTkButton(row, text="Open Source", width=95, state="normal" if item.source_url else "disabled", command=lambda value=item.source_url: webbrowser.open(value)).grid(row=0, column=2, padx=5, pady=8)
            ctk.CTkButton(row, text="Remove", width=75, command=lambda value=item.launch_id: self.remove_launch(value)).grid(row=0, column=3, padx=(5, 10), pady=8)

    def change_stage(self, launch_id, stage):
        self.service.update_stage(launch_id, stage)
        self.refresh_launches()

    def remove_launch(self, launch_id):
        self.service.remove(launch_id)
        self.refresh_launches()
