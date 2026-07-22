"""OpportunityLab Results Panel."""

import customtkinter as ctk


class ResultsPanel(ctk.CTkFrame):
    def __init__(self, master, on_selected=None):
        super().__init__(master)
        self.on_selected = on_selected
        self.cards = []
        self.group_frames = {}
        self.group_labels = {}
        self.group_counts = {}
        self.build_ui()

    def build_ui(self):
        title = ctk.CTkLabel(
            self,
            text="Search Results",
            font=("Segoe UI", 18, "bold")
        )
        title.pack(anchor="w", padx=10, pady=(10, 5))

        self.results_list = ctk.CTkScrollableFrame(self)
        self.results_list.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(0, 10)
        )

    def clear(self):
        for widget in self.results_list.winfo_children():
            widget.destroy()
        self.cards.clear()
        self.group_frames.clear()
        self.group_labels.clear()
        self.group_counts.clear()

    def score_colour(self, score):
        if score >= 90:
            return "#2ECC71"
        if score >= 75:
            return "#3498DB"
        if score >= 50:
            return "#F1C40F"
        return "#E74C3C"

    def _group_for(self, source):
        label = str(source).strip() or "Unknown Source"
        key = label.casefold()

        if key not in self.group_frames:
            group = ctk.CTkFrame(self.results_list)
            group.pack(fill="x", padx=2, pady=(5, 10))

            heading = ctk.CTkLabel(
                group,
                text=f"{label} (0)",
                anchor="w",
                font=("Segoe UI", 14, "bold"),
            )
            heading.pack(fill="x", padx=10, pady=(8, 3))

            card_area = ctk.CTkFrame(group, fg_color="transparent")
            card_area.pack(fill="x", padx=5, pady=(0, 5))

            self.group_frames[key] = card_area
            self.group_labels[key] = (heading, label)
            self.group_counts[key] = 0

        self.group_counts[key] += 1
        heading, label = self.group_labels[key]
        heading.configure(text=f"{label} ({self.group_counts[key]})")
        return self.group_frames[key]

    def add_opportunity(self, opportunity):
        group = self._group_for(getattr(opportunity, "source", ""))

        card = ctk.CTkFrame(group, cursor="hand2")
        card.pack(fill="x", padx=5, pady=5)

        badge = ctk.CTkLabel(
            card,
            text=str(opportunity.score),
            width=45,
            fg_color=self.score_colour(opportunity.score),
            corner_radius=8,
            text_color="white",
            font=("Segoe UI", 14, "bold")
        )
        badge.pack(side="left", padx=10, pady=10)

        text_area = ctk.CTkFrame(card, fg_color="transparent")
        text_area.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 8),
            pady=7
        )

        source = ctk.CTkLabel(
            text_area,
            text=str(getattr(opportunity, "source", "Unknown Source")),
            anchor="w",
            text_color=("gray35", "gray70"),
            font=("Segoe UI", 11, "bold")
        )
        source.pack(fill="x", anchor="w")

        title = ctk.CTkLabel(
            text_area,
            text=opportunity.title,
            anchor="w",
            justify="left",
            wraplength=300
        )
        title.pack(fill="x", anchor="w", pady=(2, 0))

        for widget in (card, badge, text_area, source, title):
            widget.bind(
                "<Button-1>",
                lambda event, item=opportunity: self.select(item)
            )

        self.cards.append(card)

    def select(self, opportunity):
        if self.on_selected:
            self.on_selected(opportunity)
