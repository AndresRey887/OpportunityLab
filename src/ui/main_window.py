"""
OpportunityLab Main Window

Package-019B-03:
MainWindow delegates all AI work to AIController.
"""

import queue
import webbrowser

import customtkinter as ctk

from src.ai.ai_controller import AIController
from src.core.app_logger import get_logger
from src.core.search_service import SearchService
from src.core.task_manager import BackgroundTaskManager
from src.reminders.reminder_service import ReminderService
from src.scheduling.scheduled_search_monitor import ScheduledSearchMonitor
from src.scheduling.scheduled_search_runner import ScheduledSearchRunner
from src.scheduling.search_scheduler import SearchScheduler
from src.services.search_history_service import SearchHistoryService
from src.tracking.tracking_service import TrackingService
from src.workflows.workflow_service import WorkflowService
from src.ui.details_panel import DetailsPanel
from src.ui.filter_window import FilterWindow
from src.ui.related_search_panel import RelatedSearchPanel
from src.ui.results_panel import ResultsPanel
from src.ui.scheduled_search_window import ScheduledSearchWindow
from src.ui.tracking_window import TrackingWindow
from src.ui.checklist_window import ChecklistWindow
from src.version import VERSION_INFO


logger = get_logger("MainWindow")


class MainWindow(ctk.CTk):

    def __init__(self):

        super().__init__()

        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.title(VERSION_INFO.window_title)
        self.geometry("1450x850")
        self.minsize(1200, 700)

        logger.info("Application starting: %s", VERSION_INFO.full_label)

        self.search_service = SearchService()
        self.search_history = SearchHistoryService()
        self.tracking_service = TrackingService()
        self.reminder_service = ReminderService(self.tracking_service)
        self.workflow_service = WorkflowService()

        self.scheduled_search_service = SearchService()
        self.search_scheduler = SearchScheduler()
        self.scheduled_result_queue = queue.Queue()
        self.scheduled_search_runner = ScheduledSearchRunner(
            self.search_scheduler,
            self.scheduled_search_service,
        )
        self.scheduled_search_monitor = ScheduledSearchMonitor(
            self.scheduled_search_runner,
            check_interval_seconds=60.0,
            on_results=self.queue_scheduled_results,
        )

        self.ai_controller = AIController()
        self.task_manager = BackgroundTaskManager(self)
        logger.info("Background task manager ready")
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.filter_window = None
        self.scheduled_search_window = None
        self.tracking_window = None
        self.analysis_running = False
        self.related_search_running = False
        self.selected_opportunity = None

        self.suggestion_buttons = []

        self.build_ui()
        self.refresh_tracking_notice()
        self.scheduled_search_monitor.start()
        self.after(1000, self.poll_scheduled_results)
        logger.info("Scheduled search monitor started")

    def queue_scheduled_results(self, results):
        self.scheduled_result_queue.put(list(results))

    def poll_scheduled_results(self):
        latest_results = None

        while True:
            try:
                latest_results = self.scheduled_result_queue.get_nowait()
            except queue.Empty:
                break

        if latest_results:
            new_count = sum(
                result.new_opportunity_count
                for result in latest_results
                if result.succeeded
            )
            failed_count = sum(
                not result.succeeded
                for result in latest_results
            )
            self.status.configure(
                text=(
                    f"Scheduled searches finished   "
                    f"New opportunities: {new_count}   "
                    f"Failed: {failed_count}"
                )
            )

        self.after(1000, self.poll_scheduled_results)

    def refresh_tracking_notice(self):
        due_count = len(self.reminder_service.due())

        self.tracking_button.configure(
            text=(
                f"Tracked ({due_count} due)..."
                if due_count
                else "Tracked..."
            )
        )

        if due_count:
            self.status.configure(
                text=f"Follow-up reminders due: {due_count}"
            )

    def build_ui(self):

        #
        # Search Area
        #

        top = ctk.CTkFrame(self)

        top.pack(
            fill="x",
            padx=10,
            pady=10
        )

        top.grid_columnconfigure(0, weight=1)

        search_row = ctk.CTkFrame(
            top,
            fg_color="transparent"
        )

        search_row.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=5,
            pady=5
        )

        search_row.grid_columnconfigure(0, weight=1)

        self.search_box = ctk.CTkEntry(
            search_row,
            placeholder_text="Search for opportunities...",
            height=38
        )

        self.search_box.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(0, 5)
        )

        self.search_box.bind(
            "<Return>",
            lambda event: self.perform_search()
        )

        self.search_box.bind(
            "<KeyRelease>",
            self.on_search_box_changed
        )

        self.search_box.bind(
            "<FocusIn>",
            lambda event: self.show_search_suggestions()
        )

        self.search_box.bind(
            "<Escape>",
            lambda event: self.hide_search_suggestions()
        )

        self.search_button = ctk.CTkButton(
            search_row,
            text="Search",
            width=105,
            height=38,
            command=self.perform_search
        )

        self.search_button.grid(
            row=0,
            column=1,
            padx=5
        )

        self.recent_button = ctk.CTkButton(
            search_row,
            text="Recent",
            width=95,
            height=38,
            command=self.toggle_recent_searches
        )

        self.recent_button.grid(
            row=0,
            column=2,
            padx=5
        )

        self.related_button = ctk.CTkButton(
            search_row,
            text="Related",
            width=105,
            height=38,
            command=self.toggle_related_intelligence
        )

        self.related_button.grid(
            row=0,
            column=3,
            padx=5
        )

        self.filter_button = ctk.CTkButton(
            search_row,
            text="Filters...",
            width=105,
            height=38,
            command=self.open_filters
        )

        self.filter_button.grid(
            row=0,
            column=4,
            padx=5
        )

        self.schedule_button = ctk.CTkButton(
            search_row,
            text="Schedules...",
            width=105,
            height=38,
            command=self.open_scheduled_searches
        )

        self.schedule_button.grid(
            row=0,
            column=5,
            padx=5
        )

        self.tracking_button = ctk.CTkButton(
            search_row,
            text="Tracked...",
            width=105,
            height=38,
            command=self.open_tracking_window
        )

        self.tracking_button.grid(
            row=0,
            column=6,
            padx=(5, 0)
        )

        #
        # Search Suggestions
        #

        self.suggestion_panel = ctk.CTkFrame(
            top
        )

        self.suggestion_panel.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=5,
            pady=(0, 5)
        )

        self.suggestion_panel.grid_columnconfigure(
            0,
            weight=1
        )

        suggestion_header = ctk.CTkFrame(
            self.suggestion_panel,
            fg_color="transparent"
        )

        suggestion_header.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=8,
            pady=(6, 2)
        )

        suggestion_header.grid_columnconfigure(
            0,
            weight=1
        )

        self.suggestion_title = ctk.CTkLabel(
            suggestion_header,
            text="Recent Searches",
            anchor="w",
            font=("Segoe UI", 13, "bold")
        )

        self.suggestion_title.grid(
            row=0,
            column=0,
            sticky="w"
        )

        self.clear_history_button = ctk.CTkButton(
            suggestion_header,
            text="Clear History",
            width=95,
            height=26,
            command=self.clear_search_history
        )

        self.clear_history_button.grid(
            row=0,
            column=1,
            sticky="e"
        )

        self.suggestion_list = ctk.CTkFrame(
            self.suggestion_panel,
            fg_color="transparent"
        )

        self.suggestion_list.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=6,
            pady=(2, 6)
        )

        self.suggestion_list.grid_columnconfigure(
            0,
            weight=1
        )

        self.suggestion_panel.grid_remove()

        #
        # Related Intelligence
        #

        self.related_panel = RelatedSearchPanel(
            self,
            on_generate=self.generate_related_searches,
            on_search=self.run_related_search
        )

        self.related_panel.pack(
            fill="x",
            padx=10,
            pady=(0, 8)
        )

        self.related_panel.pack_forget()

        #
        # Main Body
        #

        body = ctk.CTkFrame(self)

        body.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(0, 10)
        )

        body.grid_columnconfigure(0, weight=2)
        body.grid_columnconfigure(1, weight=3)
        body.grid_columnconfigure(2, weight=3)
        body.grid_rowconfigure(0, weight=1)

        self.results = ResultsPanel(
            body,
            on_selected=self.show_details
        )

        self.results.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=5,
            pady=5
        )

        self.details = DetailsPanel(
            body,
            on_analyze=self.start_analysis
        )

        self.details.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=5,
            pady=5
        )

        intelligence_container = ctk.CTkFrame(
            body
        )

        intelligence_container.grid(
            row=0,
            column=2,
            sticky="nsew",
            padx=5,
            pady=5
        )

        intelligence_container.grid_columnconfigure(
            0,
            weight=1
        )

        intelligence_container.grid_rowconfigure(
            1,
            weight=1
        )

        ctk.CTkLabel(
            intelligence_container,
            text="Opportunity Intelligence",
            font=("Segoe UI", 20, "bold")
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=15,
            pady=(12, 6)
        )

        self.intelligence = ctk.CTkScrollableFrame(
            intelligence_container
        )

        self.intelligence.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=10,
            pady=(0, 10)
        )

        self.intelligence.grid_columnconfigure(
            0,
            weight=1
        )

        self.build_intelligence_panel()

        self.progress = ctk.CTkProgressBar(
            self
        )

        self.progress.pack(
            fill="x",
            padx=10
        )

        self.progress.set(0)

        self.status = ctk.CTkLabel(
            self,
            text="Ready",
            anchor="w",
            font=("Segoe UI", 13)
        )

        self.status.pack(
            fill="x",
            padx=10,
            pady=(5, 10)
        )

    def build_intelligence_panel(self):

        self.score_card = ctk.CTkFrame(
            self.intelligence
        )

        self.score_card.pack(
            fill="x",
            padx=5,
            pady=(5, 8)
        )

        self.stars_label = ctk.CTkLabel(
            self.score_card,
            text="☆☆☆☆☆",
            font=("Segoe UI", 24, "bold")
        )

        self.stars_label.pack(
            anchor="w",
            padx=12,
            pady=(12, 0)
        )

        self.value_label = ctk.CTkLabel(
            self.score_card,
            text="Opportunity Value: --",
            font=("Segoe UI", 20, "bold"),
            anchor="w"
        )

        self.value_label.pack(
            fill="x",
            padx=12,
            pady=(0, 12)
        )

        metrics = ctk.CTkFrame(
            self.intelligence
        )

        metrics.pack(
            fill="x",
            padx=5,
            pady=8
        )

        metrics.grid_columnconfigure(
            1,
            weight=1
        )

        self.rule_score_value = self.add_metric(
            metrics,
            0,
            "Rule Score",
            "--"
        )

        self.confidence_value = self.add_metric(
            metrics,
            1,
            "AI Confidence",
            "--"
        )

        self.category_value = self.add_metric(
            metrics,
            2,
            "Category",
            "Not analysed"
        )

        self.difficulty_value = self.add_metric(
            metrics,
            3,
            "Difficulty",
            "Unknown"
        )

        self.time_value = self.add_metric(
            metrics,
            4,
            "Time Sensitivity",
            "Unknown"
        )

        self.effort_value = self.add_metric(
            metrics,
            5,
            "Estimated Effort",
            "Unknown"
        )

        self.summary_text = self.add_text_card(
            "Summary",
            "Select an opportunity, then click Analyse Opportunity."
        )

        self.positives_text = self.add_text_card(
            "Strengths",
            "No analysis available."
        )

        self.negatives_text = self.add_text_card(
            "Things to Consider",
            "No analysis available."
        )

        self.warnings_text = self.add_text_card(
            "Warnings",
            "No warnings available."
        )

        self.tags_text = self.add_text_card(
            "Tags",
            "No tags available."
        )

        self.action_text = self.add_text_card(
            "Recommended Action",
            "Analyse the selected opportunity to receive a recommendation."
        )

        action_card = ctk.CTkFrame(
            self.intelligence
        )

        action_card.pack(
            fill="x",
            padx=5,
            pady=8
        )

        ctk.CTkLabel(
            action_card,
            text="Available Actions",
            font=("Segoe UI", 17, "bold")
        ).pack(
            anchor="w",
            padx=12,
            pady=(12, 8)
        )

        self.open_website_button = ctk.CTkButton(
            action_card,
            text="Open Website",
            command=self.open_selected_website,
            state="disabled"
        )

        self.open_website_button.pack(
            fill="x",
            padx=12,
            pady=4
        )

        self.track_opportunity_button = ctk.CTkButton(
            action_card,
            text="Track Opportunity",
            command=self.track_selected_opportunity,
            state="disabled"
        )

        self.track_opportunity_button.pack(
            fill="x",
            padx=12,
            pady=4
        )

        self.draft_email_button = ctk.CTkButton(
            action_card,
            text="Draft Email — Coming Soon",
            state="disabled"
        )

        self.draft_email_button.pack(
            fill="x",
            padx=12,
            pady=4
        )

        self.draft_application_button = ctk.CTkButton(
            action_card,
            text="Draft Application — Coming Soon",
            state="disabled"
        )

        self.draft_application_button.pack(
            fill="x",
            padx=12,
            pady=4
        )

        self.checklist_button = ctk.CTkButton(
            action_card,
            text="Create Checklist",
            command=self.open_selected_checklist,
            state="disabled"
        )

        self.checklist_button.pack(
            fill="x",
            padx=12,
            pady=(4, 12)
        )

        self.source_label = ctk.CTkLabel(
            self.intelligence,
            text="",
            anchor="w",
            font=("Segoe UI", 11)
        )

        self.source_label.pack(
            fill="x",
            padx=10,
            pady=(2, 10)
        )

    def add_metric(
        self,
        parent,
        row,
        name,
        value
    ):

        ctk.CTkLabel(
            parent,
            text=name,
            anchor="w",
            font=("Segoe UI", 13, "bold")
        ).grid(
            row=row,
            column=0,
            sticky="w",
            padx=(12, 8),
            pady=5
        )

        value_label = ctk.CTkLabel(
            parent,
            text=value,
            anchor="e",
            justify="right",
            wraplength=220
        )

        value_label.grid(
            row=row,
            column=1,
            sticky="e",
            padx=(8, 12),
            pady=5
        )

        return value_label

    def add_text_card(
        self,
        title,
        initial_text
    ):

        card = ctk.CTkFrame(
            self.intelligence
        )

        card.pack(
            fill="x",
            padx=5,
            pady=8
        )

        ctk.CTkLabel(
            card,
            text=title,
            font=("Segoe UI", 17, "bold"),
            anchor="w"
        ).pack(
            fill="x",
            padx=12,
            pady=(12, 5)
        )

        label = ctk.CTkLabel(
            card,
            text=initial_text,
            anchor="w",
            justify="left",
            wraplength=390
        )

        label.pack(
            fill="x",
            padx=12,
            pady=(0, 12)
        )

        return label

    #
    # Related Intelligence
    #

    def toggle_related_intelligence(self):

        if self.related_panel.winfo_ismapped():

            self.related_panel.pack_forget()

            self.related_button.configure(
                text="Related"
            )

            return

        self.hide_search_suggestions()

        self.related_panel.pack(
            fill="x",
            padx=10,
            pady=(0, 8),
            before=self.winfo_children()[-3]
        )

        self.related_button.configure(
            text="Hide Related"
        )

        history = self.get_history_suggestions(
            self.search_box.get().strip()
        )

        self.related_panel.show_history_only(
            history
        )

        if self.search_box.get().strip():
            self.generate_related_searches()

    def generate_related_searches(self):

        if self.related_search_running:
            return

        query = self.search_box.get().strip()

        if not query:

            self.related_panel.show_error(
                "Enter a search phrase first.",
                self.search_history.get_recent_searches(
                    limit=5
                )
            )

            return

        self.related_search_running = True

        self.related_panel.show_loading(
            query
        )

        self.related_button.configure(
            state="disabled"
        )

        self.status.configure(
            text=(
                f'Generating related searches for "{query}"...'
            )
        )

        history_suggestions = self.get_history_suggestions(query)

        self.task_manager.submit(
            name="Generate related searches",
            target=self.ai_controller.suggest_related_searches,
            args=(query,),
            kwargs={"limit": 6},
            on_success=(
                lambda suggestions,
                       current_query=query,
                       history=list(history_suggestions):
                self.finish_related_generation(
                    current_query,
                    list(suggestions or []),
                    history,
                    None
                )
            ),
            on_error=(
                lambda error,
                       current_query=query,
                       history=list(history_suggestions):
                self.finish_related_generation(
                    current_query,
                    [],
                    history,
                    str(error)
                )
            )
        )

    def finish_related_generation(
        self,
        query,
        ollama_suggestions,
        history_suggestions,
        error
    ):

        self.related_search_running = False

        self.related_button.configure(
            state="normal"
        )

        if error:

            self.related_panel.show_error(
                error,
                history_suggestions
            )

            self.status.configure(
                text="Related-search generation failed"
            )

            return

        self.related_panel.show_results(
            query,
            ollama_suggestions,
            history_suggestions
        )

        self.status.configure(
            text=(
                f"Generated "
                f"{len(ollama_suggestions)} related searches"
            )
        )

    def get_history_suggestions(
        self,
        current_query
    ):

        current_query = str(
            current_query
        ).strip().lower()

        recent = (
            self.search_history.get_recent_searches(
                limit=12
            )
        )

        suggestions = []

        for query in recent:

            cleaned = str(query).strip()

            if not cleaned:
                continue

            if cleaned.lower() == current_query:
                continue

            suggestions.append(cleaned)

            if len(suggestions) >= 5:
                break

        return suggestions

    def run_related_search(
        self,
        query
    ):

        self.search_box.delete(
            0,
            "end"
        )

        self.search_box.insert(
            0,
            query
        )

        self.status.configure(
            text=f'Searching "{query}"...'
        )

        self.after(
            100,
            self.perform_search
        )

    #
    # Search History
    #

    def on_search_box_changed(
        self,
        event=None
    ):

        ignored_keys = {
            "Return",
            "Escape",
            "Up",
            "Down",
            "Left",
            "Right",
            "Tab"
        }

        if (
            event is not None
            and event.keysym in ignored_keys
        ):
            return

        self.show_search_suggestions()

    def show_search_suggestions(self):

        text = self.search_box.get().strip()

        suggestions = (
            self.search_history.get_suggestions(
                text,
                limit=6
            )
        )

        self.populate_search_suggestions(
            suggestions,
            title=(
                "Search Suggestions"
                if text
                else "Recent Searches"
            )
        )

    def toggle_recent_searches(self):

        if self.suggestion_panel.winfo_ismapped():

            self.hide_search_suggestions()

            return

        suggestions = (
            self.search_history.get_recent_searches(
                limit=8
            )
        )

        self.populate_search_suggestions(
            suggestions,
            title="Recent Searches"
        )

    def populate_search_suggestions(
        self,
        suggestions,
        title
    ):

        for widget in (
            self.suggestion_list.winfo_children()
        ):

            widget.destroy()

        self.suggestion_buttons.clear()

        self.suggestion_title.configure(
            text=title
        )

        if not suggestions:

            ctk.CTkLabel(
                self.suggestion_list,
                text="No saved searches yet.",
                anchor="w"
            ).grid(
                row=0,
                column=0,
                sticky="ew",
                padx=8,
                pady=8
            )

        else:

            for row_number, query in enumerate(
                suggestions
            ):

                button = ctk.CTkButton(
                    self.suggestion_list,
                    text=query,
                    anchor="w",
                    height=32,
                    command=lambda selected=query: (
                        self.select_search_suggestion(
                            selected
                        )
                    )
                )

                button.grid(
                    row=row_number,
                    column=0,
                    sticky="ew",
                    padx=3,
                    pady=2
                )

                self.suggestion_buttons.append(
                    button
                )

        self.suggestion_panel.grid()

    def select_search_suggestion(
        self,
        query
    ):

        self.search_box.delete(
            0,
            "end"
        )

        self.search_box.insert(
            0,
            query
        )

        self.hide_search_suggestions()

        self.search_box.focus_set()

    def hide_search_suggestions(self):

        self.suggestion_panel.grid_remove()

    def clear_search_history(self):

        self.search_history.clear_history()

        self.populate_search_suggestions(
            [],
            title="Recent Searches"
        )

        self.status.configure(
            text="Search history cleared"
        )

    #
    # Filters
    #

    def open_filters(self):

        if self.filter_window is not None:

            try:

                if self.filter_window.winfo_exists():

                    self.filter_window.focus()

                    return

            except Exception:
                pass

        self.filter_window = FilterWindow(
            self
        )

    def open_scheduled_searches(self):

        if self.scheduled_search_window is not None:

            try:
                if self.scheduled_search_window.winfo_exists():
                    self.scheduled_search_window.focus()
                    return
            except Exception:
                pass

        self.scheduled_search_window = ScheduledSearchWindow(self)

    def open_tracking_window(self):

        if self.tracking_window is not None:

            try:
                if self.tracking_window.winfo_exists():
                    self.tracking_window.refresh_records()
                    self.tracking_window.focus()
                    return
            except Exception:
                pass

        self.tracking_window = TrackingWindow(self)

    def track_selected_opportunity(self):

        if self.selected_opportunity is None:
            return

        record, created = self.tracking_service.track(
            self.selected_opportunity
        )

        self.track_opportunity_button.configure(
            text="Tracked"
        )

        self.status.configure(
            text=(
                "Opportunity added to tracking."
                if created
                else "Opportunity is already tracked."
            )
        )

        if (
            self.tracking_window is not None
            and self.tracking_window.winfo_exists()
        ):
            self.tracking_window.refresh_records()

        self.refresh_tracking_notice()

    def open_selected_checklist(self):

        if self.selected_opportunity is None:
            return

        record, _ = self.tracking_service.track(
            self.selected_opportunity
        )
        workflow = self.workflow_service.get_or_create(record)
        ChecklistWindow(
            self,
            workflow,
            self.workflow_service,
            record.url,
        )
        self.track_opportunity_button.configure(text="Tracked")

    #
    # Search
    #

    def perform_search(self):

        query = self.search_box.get().strip()

        if not query:
            return

        self.hide_search_suggestions()

        self.search_history.add_search(
            query
        )

        self.progress.set(0.10)

        self.status.configure(
            text="Searching..."
        )

        self.search_button.configure(state="disabled")

        self.task_manager.submit(
            name="Search opportunities",
            target=self.search_service.search,
            args=(query,),
            on_success=self.finish_search,
            on_error=self.fail_search
        )

    def finish_search(self, opportunities):

        self.progress.set(0.50)

        self.status.configure(
            text="Preparing opportunities..."
        )

        self.results.clear()

        self.selected_opportunity = None
        self.details.current_opportunity = None

        self.reset_intelligence_panel()

        self.results.show_opportunities(opportunities)

        self.progress.set(1.00)
        self.search_button.configure(state="normal")

        stats = self.search_service.statistics
        search_run = self.search_service.last_search_run

        if search_run is None:
            found_count = stats.total
            unique_count = stats.total
            source_text = "Sources: unavailable"
        else:
            found_count = search_run.raw_result_count
            unique_count = search_run.unique_result_count
            successful_sources = (
                search_run.source_count - search_run.failed_source_count
            )
            source_parts = []

            for source_name, source_stats in (
                self.search_service.source_statistics.items()
            ):
                if source_stats.get("succeeded"):
                    source_parts.append(
                        f"{source_name}: {source_stats.get('result_count', 0)}"
                    )
                else:
                    source_parts.append(f"{source_name}: failed")

            source_detail = "   ".join(source_parts) or "No sources ran"
            source_text = (
                f"Sources: {successful_sources}/{search_run.source_count}   "
                f"{source_detail}"
            )

        self.status.configure(
            text=(
                f"Finished   "
                f"Found: {found_count}   "
                f"Unique: {unique_count}   "
                f"Displayed: {stats.accepted}   "
                f"Hidden: {stats.filtered}\n"
                f"{source_text}"
            )
        )

    def fail_search(self, error):

        self.progress.set(0.00)
        self.search_button.configure(state="normal")

        self.status.configure(
            text=f"Search failed: {error}"
        )

    #
    # Opportunity Selection
    #

    def show_details(
        self,
        opportunity
    ):

        self.selected_opportunity = opportunity

        self.details.show(
            opportunity
        )

        self.rule_score_value.configure(
            text=f"{opportunity.score}/100"
        )

        self.open_website_button.configure(
            state="normal"
        )
        self.checklist_button.configure(state="normal")

        tracked = self.tracking_service.is_tracked(opportunity.url)
        self.track_opportunity_button.configure(
            state="normal",
            text="Tracked" if tracked else "Track Opportunity"
        )

        saved_analysis = getattr(
            opportunity,
            "ai_analysis",
            None
        )

        if saved_analysis is not None:

            self.display_analysis(
                saved_analysis,
                cached_result=True
            )

            return

        cached_analysis = (
            self.ai_controller.get_cached_analysis(
                opportunity
            )
        )

        if cached_analysis is not None:

            opportunity.ai_analysis = (
                cached_analysis
            )

            self.display_analysis(
                cached_analysis,
                cached_result=True
            )

            return

        self.clear_analysis_for_selection(
            opportunity
        )

    def clear_analysis_for_selection(
        self,
        opportunity
    ):

        self.stars_label.configure(
            text="☆☆☆☆☆"
        )

        self.value_label.configure(
            text="Opportunity Value: --"
        )

        self.rule_score_value.configure(
            text=f"{opportunity.score}/100"
        )

        self.confidence_value.configure(
            text="--"
        )

        self.category_value.configure(
            text="Not analysed"
        )

        self.difficulty_value.configure(
            text="Unknown"
        )

        self.time_value.configure(
            text="Unknown"
        )

        self.effort_value.configure(
            text="Unknown"
        )

        self.summary_text.configure(
            text=(
                "This opportunity has not been analysed yet.\n\n"
                "Click Analyse Opportunity in the centre panel."
            )
        )

        self.positives_text.configure(
            text="No analysis available."
        )

        self.negatives_text.configure(
            text="No analysis available."
        )

        self.warnings_text.configure(
            text="No warnings available."
        )

        self.tags_text.configure(
            text="No tags available."
        )

        self.action_text.configure(
            text=(
                "Analyse the opportunity to receive "
                "a recommended next action."
            )
        )

        self.source_label.configure(
            text=""
        )

    #
    # AI Analysis
    #

    def start_analysis(
        self,
        opportunity
    ):

        if self.analysis_running:
            return

        self.analysis_running = True

        self.details.set_analysis_running(
            True
        )

        self.summary_text.configure(
            text=(
                "Analysing opportunity...\n\n"
                "Gemini is reviewing the result."
            )
        )

        self.status.configure(
            text="Analysing opportunity..."
        )

        self.task_manager.submit(
            name="Analyse opportunity",
            target=self.ai_controller.analyze,
            args=(opportunity,),
            on_success=(
                lambda analysis, selected=opportunity:
                self.finish_analysis(selected, analysis)
            ),
            on_error=(
                lambda error, selected=opportunity:
                self.fail_analysis(selected, error)
            )
        )

    def fail_analysis(
        self,
        opportunity,
        error
    ):

        self.analysis_running = False
        self.details.set_analysis_running(False)

        self.status.configure(
            text=f"Opportunity analysis failed: {error}"
        )

        if self.selected_opportunity is opportunity:
            self.summary_text.configure(
                text=f"Analysis failed.\n\n{error}"
            )

    def finish_analysis(
        self,
        opportunity,
        analysis
    ):

        self.analysis_running = False

        self.details.set_analysis_running(
            False
        )

        opportunity.ai_analysis = analysis

        self.status.configure(
            text="Opportunity analysis complete"
        )

        if self.selected_opportunity is opportunity:

            self.display_analysis(
                analysis
            )

    def display_analysis(
        self,
        analysis,
        cached_result=False
    ):

        value = self.safe_score(
            getattr(
                analysis,
                "opportunity_value",
                0
            )
        )

        confidence = self.safe_score(
            getattr(
                analysis,
                "confidence",
                0
            )
        )

        self.stars_label.configure(
            text=self.score_to_stars(
                value
            )
        )

        self.value_label.configure(
            text=f"Opportunity Value: {value}/100"
        )

        self.confidence_value.configure(
            text=f"{confidence}%"
        )

        self.category_value.configure(
            text=(
                getattr(
                    analysis,
                    "category",
                    ""
                )
                or "Not available"
            )
        )

        self.difficulty_value.configure(
            text=(
                getattr(
                    analysis,
                    "difficulty",
                    ""
                )
                or "Unknown"
            )
        )

        self.time_value.configure(
            text=(
                getattr(
                    analysis,
                    "time_sensitivity",
                    ""
                )
                or "Unknown"
            )
        )

        self.effort_value.configure(
            text=(
                getattr(
                    analysis,
                    "estimated_effort",
                    ""
                )
                or "Unknown"
            )
        )

        self.summary_text.configure(
            text=(
                getattr(
                    analysis,
                    "summary",
                    ""
                )
                or "No summary available."
            )
        )

        self.positives_text.configure(
            text=self.format_items(
                getattr(
                    analysis,
                    "positives",
                    []
                ),
                "✓",
                "No strengths identified."
            )
        )

        self.negatives_text.configure(
            text=self.format_items(
                getattr(
                    analysis,
                    "negatives",
                    []
                ),
                "•",
                "No concerns identified."
            )
        )

        self.warnings_text.configure(
            text=self.format_items(
                getattr(
                    analysis,
                    "warnings",
                    []
                ),
                "⚠",
                "No warnings identified."
            )
        )

        tags = getattr(
            analysis,
            "tags",
            []
        )

        self.tags_text.configure(
            text=(
                "   ".join(
                    f"[{tag}]"
                    for tag in tags
                )
                if tags
                else "No tags available."
            )
        )

        self.action_text.configure(
            text=(
                getattr(
                    analysis,
                    "recommended_action",
                    ""
                )
                or "No recommendation available."
            )
        )

        source_parts = []

        provider = getattr(
            analysis,
            "provider",
            ""
        )

        model = getattr(
            analysis,
            "model",
            ""
        )

        analysed_at = getattr(
            analysis,
            "analysed_at",
            ""
        )

        if provider:

            source_parts.append(
                f"Provider: {provider}"
            )

        if model:

            source_parts.append(
                f"Model: {model}"
            )

        if analysed_at:

            source_parts.append(
                f"Analysed: {analysed_at}"
            )

        if cached_result:

            source_parts.append(
                "Source: Cached analysis"
            )

        self.source_label.configure(
            text=" | ".join(
                source_parts
            )
        )

    def reset_intelligence_panel(self):

        self.selected_opportunity = None

        self.stars_label.configure(
            text="☆☆☆☆☆"
        )

        self.value_label.configure(
            text="Opportunity Value: --"
        )

        self.rule_score_value.configure(
            text="--"
        )

        self.confidence_value.configure(
            text="--"
        )

        self.category_value.configure(
            text="Not analysed"
        )

        self.difficulty_value.configure(
            text="Unknown"
        )

        self.time_value.configure(
            text="Unknown"
        )

        self.effort_value.configure(
            text="Unknown"
        )

        self.summary_text.configure(
            text=(
                "Select an opportunity, then click "
                "Analyse Opportunity."
            )
        )

        self.positives_text.configure(
            text="No analysis available."
        )

        self.negatives_text.configure(
            text="No analysis available."
        )

        self.warnings_text.configure(
            text="No warnings available."
        )

        self.tags_text.configure(
            text="No tags available."
        )

        self.action_text.configure(
            text=(
                "Analyse the selected opportunity "
                "to receive a recommendation."
            )
        )

        self.source_label.configure(
            text=""
        )

        self.open_website_button.configure(
            state="disabled"
        )

    #
    # Helpers
    #

    def score_to_stars(
        self,
        score
    ):

        filled = round(
            score / 20
        )

        filled = max(
            0,
            min(filled, 5)
        )

        return (
            "★" * filled
            + "☆" * (5 - filled)
        )

    def safe_score(
        self,
        value
    ):

        try:
            value = int(value)

        except (TypeError, ValueError):
            value = 0

        return max(
            0,
            min(value, 100)
        )

    def format_items(
        self,
        items,
        prefix,
        empty_message
    ):

        if not items:
            return empty_message

        return "\n".join(
            f"{prefix} {item}"
            for item in items
        )

    def open_selected_website(self):

        if (
            self.selected_opportunity is not None
            and self.selected_opportunity.url
        ):

            webbrowser.open(
                self.selected_opportunity.url
            )

    def on_close(self):
        """Stop background workers before closing the application."""
        logger.info("Application closing")
        self.scheduled_search_monitor.stop()
        self.task_manager.shutdown(wait=False)
        self.destroy()



if __name__ == "__main__":

    app = MainWindow()
    app.mainloop()
