"""
OpportunityLab Related Intelligence Panel

Displays related search suggestions from Ollama and
the user's existing search history.
"""

import customtkinter as ctk


class RelatedSearchPanel(ctk.CTkFrame):

    def __init__(
        self,
        master,
        on_generate=None,
        on_search=None
    ):

        super().__init__(master)

        self.on_generate = on_generate
        self.on_search = on_search

        self.current_query = ""
        self.suggestion_buttons = []

        self.build_ui()

    def build_ui(self):

        self.grid_columnconfigure(0, weight=1)

        #
        # Header
        #

        header = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        header.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=10,
            pady=(8, 4)
        )

        header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header,
            text="Related Intelligence",
            font=("Segoe UI", 17, "bold"),
            anchor="w"
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )

        self.generate_button = ctk.CTkButton(
            header,
            text="Generate Ideas",
            width=120,
            height=30,
            command=self.request_generation
        )

        self.generate_button.grid(
            row=0,
            column=1,
            padx=(5, 0)
        )

        #
        # Status
        #

        self.status_label = ctk.CTkLabel(
            self,
            text=(
                "Enter a search phrase, then generate related ideas."
            ),
            anchor="w",
            justify="left",
            wraplength=1100
        )

        self.status_label.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=12,
            pady=(0, 6)
        )

        #
        # Suggestions Area
        #

        self.sections = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.sections.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=8,
            pady=(0, 8)
        )

        self.sections.grid_columnconfigure(
            0,
            weight=1
        )

        self.sections.grid_columnconfigure(
            1,
            weight=1
        )

        #
        # Ollama Suggestions
        #

        self.ollama_frame = ctk.CTkFrame(
            self.sections
        )

        self.ollama_frame.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 4)
        )

        ctk.CTkLabel(
            self.ollama_frame,
            text="Ollama Suggestions",
            font=("Segoe UI", 14, "bold"),
            anchor="w"
        ).pack(
            fill="x",
            padx=10,
            pady=(8, 4)
        )

        self.ollama_list = ctk.CTkFrame(
            self.ollama_frame,
            fg_color="transparent"
        )

        self.ollama_list.pack(
            fill="x",
            padx=6,
            pady=(0, 8)
        )

        #
        # History Suggestions
        #

        self.history_frame = ctk.CTkFrame(
            self.sections
        )

        self.history_frame.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(4, 0)
        )

        ctk.CTkLabel(
            self.history_frame,
            text="From Your Search History",
            font=("Segoe UI", 14, "bold"),
            anchor="w"
        ).pack(
            fill="x",
            padx=10,
            pady=(8, 4)
        )

        self.history_list = ctk.CTkFrame(
            self.history_frame,
            fg_color="transparent"
        )

        self.history_list.pack(
            fill="x",
            padx=6,
            pady=(0, 8)
        )

        self.show_empty_state()

    def set_query(self, query):

        self.current_query = str(query).strip()

    def request_generation(self):

        if self.on_generate is not None:
            self.on_generate()

    def show_loading(self, query):

        self.set_query(query)

        self.generate_button.configure(
            state="disabled",
            text="Generating..."
        )

        self.status_label.configure(
            text=(
                f'Finding related searches for "{query}" '
                "using local Ollama..."
            )
        )

        self.clear_lists()

        self._add_message(
            self.ollama_list,
            "Ollama is preparing suggestions..."
        )

        self._add_message(
            self.history_list,
            "Checking previous searches..."
        )

    def show_results(
        self,
        query,
        ollama_suggestions,
        history_suggestions
    ):

        self.set_query(query)

        self.generate_button.configure(
            state="normal",
            text="Generate Again"
        )

        self.status_label.configure(
            text=(
                f'Related ideas for "{query}". '
                "Select an idea to search immediately."
            )
        )

        self.clear_lists()

        self._populate_list(
            parent=self.ollama_list,
            suggestions=ollama_suggestions,
            empty_message="Ollama returned no suggestions."
        )

        self._populate_list(
            parent=self.history_list,
            suggestions=history_suggestions,
            empty_message="No related searches in your history yet."
        )

    def show_history_only(
        self,
        history_suggestions
    ):

        self.generate_button.configure(
            state="normal",
            text="Generate Ideas"
        )

        self.status_label.configure(
            text=(
                "Enter or select a search, then use Ollama "
                "to generate related ideas."
            )
        )

        self.clear_lists()

        self._add_message(
            self.ollama_list,
            "No Ollama suggestions generated yet."
        )

        self._populate_list(
            parent=self.history_list,
            suggestions=history_suggestions,
            empty_message="No saved searches yet."
        )

    def show_error(
        self,
        message,
        history_suggestions=None
    ):

        self.generate_button.configure(
            state="normal",
            text="Try Again"
        )

        self.status_label.configure(
            text=f"Related-search generation failed: {message}"
        )

        self.clear_lists()

        self._add_message(
            self.ollama_list,
            message
        )

        self._populate_list(
            parent=self.history_list,
            suggestions=history_suggestions or [],
            empty_message="No related searches in your history."
        )

    def show_empty_state(self):

        self.clear_lists()

        self._add_message(
            self.ollama_list,
            "No Ollama suggestions generated yet."
        )

        self._add_message(
            self.history_list,
            "No search history available yet."
        )

    def clear_lists(self):

        for parent in (
            self.ollama_list,
            self.history_list
        ):

            for widget in parent.winfo_children():
                widget.destroy()

        self.suggestion_buttons.clear()

    def _populate_list(
        self,
        parent,
        suggestions,
        empty_message
    ):

        cleaned = []

        for suggestion in suggestions or []:

            text = str(suggestion).strip()

            if text and text not in cleaned:
                cleaned.append(text)

        if not cleaned:

            self._add_message(
                parent,
                empty_message
            )

            return

        for suggestion in cleaned:

            button = ctk.CTkButton(
                parent,
                text=f"Search: {suggestion}",
                anchor="w",
                height=34,
                command=lambda value=suggestion: (
                    self.select_suggestion(value)
                )
            )

            button.pack(
                fill="x",
                padx=4,
                pady=3
            )

            self.suggestion_buttons.append(
                button
            )

    def _add_message(
        self,
        parent,
        message
    ):

        ctk.CTkLabel(
            parent,
            text=message,
            anchor="w",
            justify="left",
            wraplength=500
        ).pack(
            fill="x",
            padx=8,
            pady=8
        )

    def select_suggestion(self, suggestion):

        self.status_label.configure(
            text=f'Searching "{suggestion}"...'
        )

        selected_button = None

        for button in self.suggestion_buttons:

            if button.cget("text") == f"Search: {suggestion}":

                selected_button = button

                button.configure(
                    text=f"Searching: {suggestion}",
                    fg_color="#2E8B57",
                    state="disabled"
                )

                break

        self.after(
            250,
            lambda: self._run_selected_search(
                suggestion,
                selected_button
            )
        )

    def _run_selected_search(
        self,
        suggestion,
        selected_button
    ):

        if self.on_search is not None:
            self.on_search(suggestion)

        if selected_button is not None:

            try:

                selected_button.configure(
                    text=f"Search: {suggestion}",
                    state="normal"
                )

            except Exception:
                pass