"""
OpportunityLab Details Panel

Displays opportunity information and rule scoring.
AI analysis is displayed in the main window AI panel.
"""

import webbrowser

import customtkinter as ctk


class DetailsPanel(ctk.CTkFrame):

    def __init__(self, master, on_analyze=None):

        super().__init__(master)

        self.current_url = ""
        self.current_opportunity = None
        self.on_analyze = on_analyze

        self.build_ui()

    def build_ui(self):

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        content = ctk.CTkScrollableFrame(self)

        content.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=5,
            pady=5
        )

        #
        # Heading
        #

        header = ctk.CTkFrame(content)

        header.pack(
            fill="x",
            padx=5,
            pady=5
        )

        self.score = ctk.CTkLabel(
            header,
            text="--",
            width=60,
            font=("Segoe UI", 26, "bold")
        )

        self.score.pack(
            side="left",
            padx=10,
            pady=10
        )

        self.title = ctk.CTkLabel(
            header,
            text="No Opportunity Selected",
            anchor="w",
            justify="left",
            wraplength=420,
            font=("Segoe UI", 18, "bold")
        )

        self.title.pack(
            side="left",
            fill="x",
            expand=True,
            padx=10,
            pady=10
        )

        #
        # URL
        #

        url_frame = ctk.CTkFrame(content)

        url_frame.pack(
            fill="x",
            padx=5,
            pady=(0, 5)
        )

        self.url = ctk.CTkLabel(
            url_frame,
            text="",
            anchor="w",
            justify="left",
            wraplength=500,
            cursor="hand2",
            text_color="#4da6ff"
        )

        self.url.pack(
            fill="x",
            padx=10,
            pady=10
        )

        self.url.bind(
            "<Button-1>",
            lambda event: self.open_url()
        )

        #
        # Snippet
        #

        ctk.CTkLabel(
            content,
            text="Snippet",
            font=("Segoe UI", 16, "bold")
        ).pack(
            anchor="w",
            padx=10,
            pady=(10, 5)
        )

        self.snippet = ctk.CTkTextbox(
            content,
            height=140
        )

        self.snippet.pack(
            fill="x",
            padx=5
        )

        self.snippet.configure(state="disabled")

        #
        # Rule Breakdown
        #

        ctk.CTkLabel(
            content,
            text="Rule Breakdown",
            font=("Segoe UI", 16, "bold")
        ).pack(
            anchor="w",
            padx=10,
            pady=(15, 5)
        )

        self.rules = ctk.CTkTextbox(
            content,
            height=220
        )

        self.rules.pack(
            fill="both",
            expand=True,
            padx=5,
            pady=(0, 10)
        )

        self.rules.configure(state="disabled")

        #
        # Analyse Button
        #

        self.analyze_button = ctk.CTkButton(
            content,
            text="Analyse Opportunity",
            command=self.request_analysis,
            state="disabled"
        )

        self.analyze_button.pack(
            fill="x",
            padx=5,
            pady=(5, 10)
        )

    def show(self, opportunity):

        self.current_opportunity = opportunity
        self.current_url = opportunity.url

        self.title.configure(
            text=opportunity.title
        )

        self.score.configure(
            text=str(opportunity.score)
        )

        self.url.configure(
            text=opportunity.url
        )

        self._set_textbox_text(
            self.snippet,
            opportunity.snippet
        )

        rule_lines = []

        for rule in opportunity.rule_results:

            rule_lines.append(
                f"{rule['rule']:<25} +{rule['points']}"
            )

        if not rule_lines:
            rule_lines.append("No rule results available.")

        self._set_textbox_text(
            self.rules,
            "\n".join(rule_lines)
        )

        self.analyze_button.configure(
            state="normal",
            text="Analyse Opportunity"
        )

    def request_analysis(self):

        if (
            self.current_opportunity is not None
            and self.on_analyze is not None
        ):
            self.on_analyze(self.current_opportunity)

    def set_analysis_running(self, running):

        if running:

            self.analyze_button.configure(
                state="disabled",
                text="Analysing..."
            )

        else:

            state = (
                "normal"
                if self.current_opportunity is not None
                else "disabled"
            )

            self.analyze_button.configure(
                state=state,
                text="Analyse Opportunity"
            )

    def _set_textbox_text(self, textbox, text):

        textbox.configure(state="normal")
        textbox.delete("1.0", "end")
        textbox.insert("end", text)
        textbox.configure(state="disabled")

    def open_url(self):

        if self.current_url:
            webbrowser.open(self.current_url)