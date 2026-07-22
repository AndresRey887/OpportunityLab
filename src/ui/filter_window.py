"""
OpportunityLab Filter Manager

Provides an interactive window for managing search filters.
"""

from urllib.parse import urlparse

import customtkinter as ctk


class FilterWindow(ctk.CTkToplevel):

    def __init__(self, master=None):

        super().__init__(master)

        self.title("Search Filters")
        self.geometry("650x720")
        self.minsize(560, 600)

        self.transient(master)

        self.filter_engine = self._get_filter_engine()

        self.pending_domains = []
        self.pending_keywords = []
        self.available_sources = []
        self.source_variables = {}

        self.selected_domain = ctk.StringVar(value="")
        self.selected_keyword = ctk.StringVar(value="")

        self._load_filters()
        self.build_ui()

    def _get_filter_engine(self):

        try:
            return self.master.search_service.filter_engine

        except AttributeError:
            return None

    def _load_filters(self):

        if self.filter_engine is None:

            self.pending_domains = []
            self.pending_keywords = []
            self.available_sources = []

            return

        self.pending_domains = (
            self.filter_engine.get_blocked_domains()
        )

        self.pending_keywords = (
            self.filter_engine.get_blocked_keywords()
        )

        try:
            self.available_sources = (
                self.master.search_service.registry.all_names()
            )
        except AttributeError:
            self.available_sources = []

        allowed_sources = {
            source.casefold()
            for source in self.filter_engine.get_allowed_sources()
        }

        self.source_variables = {
            source: ctk.BooleanVar(
                value=(
                    not allowed_sources
                    or source.casefold() in allowed_sources
                )
            )
            for source in self.available_sources
        }

    def build_ui(self):

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        content = ctk.CTkScrollableFrame(self)

        content.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=10,
            pady=(10, 5)
        )

        ctk.CTkLabel(
            content,
            text="Search Filters",
            font=("Segoe UI", 22, "bold")
        ).pack(
            anchor="w",
            padx=10,
            pady=(10, 5)
        )

        ctk.CTkLabel(
            content,
            text="Control which search results OpportunityLab displays.",
            anchor="w"
        ).pack(
            fill="x",
            padx=10,
            pady=(0, 10)
        )

        #
        # General Filters
        #

        general = ctk.CTkFrame(content)

        general.pack(
            fill="x",
            padx=10,
            pady=10
        )

        ctk.CTkLabel(
            general,
            text="General Filters",
            font=("Segoe UI", 16, "bold")
        ).pack(
            anchor="w",
            padx=10,
            pady=(10, 5)
        )

        self.au_only = ctk.CTkCheckBox(
            general,
            text="Australia Only — coming soon",
            state="disabled"
        )

        self.au_only.pack(
            anchor="w",
            padx=20,
            pady=4
        )

        self.english = ctk.CTkCheckBox(
            general,
            text="English Results — coming soon",
            state="disabled"
        )

        self.english.pack(
            anchor="w",
            padx=20,
            pady=(4, 10)
        )

        #
        # Result Sources
        #

        sources = ctk.CTkFrame(content)

        sources.pack(
            fill="x",
            padx=10,
            pady=10
        )

        ctk.CTkLabel(
            sources,
            text="Result Sources",
            font=("Segoe UI", 16, "bold")
        ).pack(
            anchor="w",
            padx=10,
            pady=(10, 2)
        )

        ctk.CTkLabel(
            sources,
            text="Choose which sources can appear in the results.",
            anchor="w"
        ).pack(
            fill="x",
            padx=10,
            pady=(0, 6)
        )

        for source in self.available_sources:
            ctk.CTkCheckBox(
                sources,
                text=source,
                variable=self.source_variables[source]
            ).pack(
                anchor="w",
                padx=20,
                pady=4
            )

        if not self.available_sources:
            ctk.CTkLabel(
                sources,
                text="No discovery sources are available.",
                anchor="w"
            ).pack(
                fill="x",
                padx=20,
                pady=(4, 10)
            )

        #
        # Blocked Domains
        #

        domains = ctk.CTkFrame(content)

        domains.pack(
            fill="x",
            padx=10,
            pady=10
        )

        ctk.CTkLabel(
            domains,
            text="Blocked Domains",
            font=("Segoe UI", 16, "bold")
        ).pack(
            anchor="w",
            padx=10,
            pady=(10, 2)
        )

        ctk.CTkLabel(
            domains,
            text="Results from matching domains will be hidden.",
            anchor="w"
        ).pack(
            fill="x",
            padx=10,
            pady=(0, 8)
        )

        self.domain_list = ctk.CTkScrollableFrame(
            domains,
            height=150
        )

        self.domain_list.pack(
            fill="x",
            padx=10,
            pady=(0, 10)
        )

        domain_entry_row = ctk.CTkFrame(
            domains,
            fg_color="transparent"
        )

        domain_entry_row.pack(
            fill="x",
            padx=10,
            pady=(0, 5)
        )

        self.domain_box = ctk.CTkEntry(
            domain_entry_row,
            placeholder_text="Enter a domain, for example reddit.com"
        )

        self.domain_box.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 5)
        )

        self.domain_box.bind(
            "<Return>",
            lambda event: self.add_domain()
        )

        ctk.CTkButton(
            domain_entry_row,
            text="Add Domain",
            width=120,
            command=self.add_domain
        ).pack(side="left")

        ctk.CTkButton(
            domains,
            text="Remove Selected",
            command=self.remove_selected_domain
        ).pack(
            anchor="e",
            padx=10,
            pady=(0, 10)
        )

        #
        # Blocked Keywords
        #

        keywords = ctk.CTkFrame(content)

        keywords.pack(
            fill="x",
            padx=10,
            pady=10
        )

        ctk.CTkLabel(
            keywords,
            text="Blocked Keywords",
            font=("Segoe UI", 16, "bold")
        ).pack(
            anchor="w",
            padx=10,
            pady=(10, 2)
        )

        ctk.CTkLabel(
            keywords,
            text="Results containing these words or phrases will be hidden.",
            anchor="w"
        ).pack(
            fill="x",
            padx=10,
            pady=(0, 8)
        )

        self.keyword_list = ctk.CTkScrollableFrame(
            keywords,
            height=150
        )

        self.keyword_list.pack(
            fill="x",
            padx=10,
            pady=(0, 10)
        )

        keyword_entry_row = ctk.CTkFrame(
            keywords,
            fg_color="transparent"
        )

        keyword_entry_row.pack(
            fill="x",
            padx=10,
            pady=(0, 5)
        )

        self.keyword_box = ctk.CTkEntry(
            keyword_entry_row,
            placeholder_text="Enter a word or phrase"
        )

        self.keyword_box.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 5)
        )

        self.keyword_box.bind(
            "<Return>",
            lambda event: self.add_keyword()
        )

        ctk.CTkButton(
            keyword_entry_row,
            text="Add Keyword",
            width=120,
            command=self.add_keyword
        ).pack(side="left")

        ctk.CTkButton(
            keywords,
            text="Remove Selected",
            command=self.remove_selected_keyword
        ).pack(
            anchor="e",
            padx=10,
            pady=(0, 10)
        )

        #
        # Status Message
        #

        self.message = ctk.CTkLabel(
            content,
            text="",
            anchor="w"
        )

        self.message.pack(
            fill="x",
            padx=15,
            pady=(0, 10)
        )

        #
        # Fixed Footer
        #

        footer = ctk.CTkFrame(self)

        footer.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=10,
            pady=(5, 10)
        )

        ctk.CTkButton(
            footer,
            text="Apply",
            command=self.apply_filters
        ).pack(
            side="right",
            padx=5,
            pady=10
        )

        ctk.CTkButton(
            footer,
            text="Close",
            command=self.destroy
        ).pack(
            side="right",
            padx=5,
            pady=10
        )

        self.refresh_domain_list()
        self.refresh_keyword_list()

    def normalize_domain(self, value):

        value = value.strip().lower()

        if not value:
            return ""

        if "://" in value:

            try:
                hostname = urlparse(value).hostname

                if hostname:
                    value = hostname

            except ValueError:
                return ""

        value = value.split("/")[0]

        if value.startswith("www."):
            value = value[4:]

        return value.strip(".")

    def add_domain(self):

        domain = self.normalize_domain(
            self.domain_box.get()
        )

        if not domain:

            self.message.configure(
                text="Enter a valid domain."
            )

            return

        if domain in self.pending_domains:

            self.message.configure(
                text=f"{domain} is already in the list."
            )

            return

        self.pending_domains.append(domain)
        self.pending_domains.sort()

        self.domain_box.delete(0, "end")
        self.selected_domain.set(domain)

        self.message.configure(
            text=f"Added {domain}. Click Apply to save."
        )

        self.refresh_domain_list()

    def remove_selected_domain(self):

        domain = self.selected_domain.get()

        if not domain:

            self.message.configure(
                text="Select a domain before removing it."
            )

            return

        if domain in self.pending_domains:
            self.pending_domains.remove(domain)

        self.selected_domain.set("")

        self.message.configure(
            text=f"Removed {domain}. Click Apply to save."
        )

        self.refresh_domain_list()

    def add_keyword(self):

        keyword = self.keyword_box.get().strip().lower()

        if not keyword:

            self.message.configure(
                text="Enter a keyword or phrase."
            )

            return

        if keyword in self.pending_keywords:

            self.message.configure(
                text=f"{keyword} is already in the list."
            )

            return

        self.pending_keywords.append(keyword)
        self.pending_keywords.sort()

        self.keyword_box.delete(0, "end")
        self.selected_keyword.set(keyword)

        self.message.configure(
            text=f"Added {keyword}. Click Apply to save."
        )

        self.refresh_keyword_list()

    def remove_selected_keyword(self):

        keyword = self.selected_keyword.get()

        if not keyword:

            self.message.configure(
                text="Select a keyword before removing it."
            )

            return

        if keyword in self.pending_keywords:
            self.pending_keywords.remove(keyword)

        self.selected_keyword.set("")

        self.message.configure(
            text=f"Removed {keyword}. Click Apply to save."
        )

        self.refresh_keyword_list()

    def refresh_domain_list(self):

        for widget in self.domain_list.winfo_children():
            widget.destroy()

        if not self.pending_domains:

            ctk.CTkLabel(
                self.domain_list,
                text="No blocked domains.",
                anchor="w"
            ).pack(
                fill="x",
                padx=10,
                pady=10
            )

            return

        for domain in self.pending_domains:

            row = ctk.CTkFrame(self.domain_list)

            row.pack(
                fill="x",
                padx=5,
                pady=3
            )

            ctk.CTkRadioButton(
                row,
                text=domain,
                variable=self.selected_domain,
                value=domain
            ).pack(
                anchor="w",
                padx=10,
                pady=8
            )

    def refresh_keyword_list(self):

        for widget in self.keyword_list.winfo_children():
            widget.destroy()

        if not self.pending_keywords:

            ctk.CTkLabel(
                self.keyword_list,
                text="No blocked keywords.",
                anchor="w"
            ).pack(
                fill="x",
                padx=10,
                pady=10
            )

            return

        for keyword in self.pending_keywords:

            row = ctk.CTkFrame(self.keyword_list)

            row.pack(
                fill="x",
                padx=5,
                pady=3
            )

            ctk.CTkRadioButton(
                row,
                text=keyword,
                variable=self.selected_keyword,
                value=keyword
            ).pack(
                anchor="w",
                padx=10,
                pady=8
            )

    def apply_filters(self):

        if self.filter_engine is None:

            self.message.configure(
                text="Filter Engine could not be found."
            )

            return

        selected_sources = [
            source
            for source, variable in self.source_variables.items()
            if variable.get()
        ]

        if self.available_sources and not selected_sources:
            self.message.configure(
                text="Select at least one result source."
            )
            return

        if len(selected_sources) == len(self.available_sources):
            self.filter_engine.clear_allowed_sources()
        else:
            self.filter_engine.set_allowed_sources(selected_sources)

        self.filter_engine.set_blocked_domains(
            self.pending_domains
        )

        self.filter_engine.set_blocked_keywords(
            self.pending_keywords
        )

        self.message.configure(
            text=(
                f"Applied {len(self.pending_domains)} domains and "
                f"{len(self.pending_keywords)} keywords. "
                f"Sources: {len(selected_sources)}."
            )
        )
