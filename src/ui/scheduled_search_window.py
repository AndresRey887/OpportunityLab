"""Window for creating and managing scheduled searches."""

from __future__ import annotations

import customtkinter as ctk

from src.scheduling.search_schedule import SearchSchedule


class ScheduledSearchWindow(ctk.CTkToplevel):
    INTERVALS = {
        "30 minutes": 30,
        "1 hour": 60,
        "6 hours": 360,
        "12 hours": 720,
        "24 hours": 1440,
    }

    def __init__(self, master=None):
        super().__init__(master)
        self.title("Scheduled Searches")
        self.geometry("780x820")
        self.minsize(660, 680)
        self.transient(master)

        self.scheduler = master.search_scheduler
        self.runner = master.scheduled_search_runner
        self.history_store = master.scheduled_search_runner.history_store
        self.available_sources = master.search_service.registry.all_names()
        self.source_variables = {
            source: ctk.BooleanVar(value=True)
            for source in self.available_sources
        }

        self.build_ui()
        self.refresh_schedules()
        self.refresh_history()

    def build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        form = ctk.CTkFrame(self)
        form.grid(row=0, column=0, sticky="ew", padx=12, pady=12)
        form.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            form,
            text="Create Scheduled Search",
            font=("Segoe UI", 20, "bold"),
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=12, pady=(12, 8))

        self.query_entry = ctk.CTkEntry(
            form,
            placeholder_text="Search query",
            height=38,
        )
        self.query_entry.grid(row=1, column=0, sticky="ew", padx=12, pady=6)

        self.interval_menu = ctk.CTkOptionMenu(
            form,
            values=list(self.INTERVALS),
        )
        self.interval_menu.set("1 hour")
        self.interval_menu.grid(row=1, column=1, padx=12, pady=6)

        source_frame = ctk.CTkFrame(form, fg_color="transparent")
        source_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=12, pady=6)

        ctk.CTkLabel(
            source_frame,
            text="Sources",
            font=("Segoe UI", 13, "bold"),
        ).pack(anchor="w", pady=(0, 4))

        for source in self.available_sources:
            ctk.CTkCheckBox(
                source_frame,
                text=source,
                variable=self.source_variables[source],
            ).pack(side="left", padx=(0, 14), pady=4)

        self.message = ctk.CTkLabel(form, text="", anchor="w")
        self.message.grid(row=3, column=0, sticky="ew", padx=12, pady=6)

        ctk.CTkButton(
            form,
            text="Add Schedule",
            width=130,
            command=self.add_schedule,
        ).grid(row=3, column=1, padx=12, pady=8)

        list_frame = ctk.CTkFrame(self)
        list_frame.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 12))
        list_frame.grid_columnconfigure(0, weight=1)
        list_frame.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            list_frame,
            text="Saved Schedules",
            font=("Segoe UI", 17, "bold"),
        ).grid(row=0, column=0, sticky="w", padx=12, pady=(12, 6))

        self.schedule_list = ctk.CTkScrollableFrame(list_frame)
        self.schedule_list.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

        history_frame = ctk.CTkFrame(self)
        history_frame.grid(row=2, column=0, sticky="nsew", padx=12, pady=(0, 12))
        history_frame.grid_columnconfigure(0, weight=1)
        history_frame.grid_rowconfigure(1, weight=1)

        history_header = ctk.CTkFrame(history_frame, fg_color="transparent")
        history_header.grid(row=0, column=0, sticky="ew", padx=12, pady=(10, 4))
        history_header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            history_header,
            text="Recent Scheduled Results",
            font=("Segoe UI", 17, "bold"),
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkButton(
            history_header,
            text="Refresh",
            width=85,
            command=self.refresh_history,
        ).grid(row=0, column=1, sticky="e")

        self.history_list = ctk.CTkScrollableFrame(history_frame)
        self.history_list.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

    def add_schedule(self):
        query = self.query_entry.get().strip()
        selected_sources = [
            source
            for source, variable in self.source_variables.items()
            if variable.get()
        ]

        if not query:
            self.message.configure(text="Enter a search query.")
            return

        if not selected_sources:
            self.message.configure(text="Select at least one source.")
            return

        schedule = SearchSchedule(
            query=query,
            interval_minutes=self.INTERVALS[self.interval_menu.get()],
            source_names=selected_sources,
        )
        self.scheduler.add(schedule)
        self.query_entry.delete(0, "end")
        self.message.configure(text="Schedule added.")
        self.refresh_schedules()

    def refresh_schedules(self):
        for widget in self.schedule_list.winfo_children():
            widget.destroy()

        schedules = self.scheduler.all()
        if not schedules:
            ctk.CTkLabel(
                self.schedule_list,
                text="No scheduled searches.",
                anchor="w",
            ).pack(fill="x", padx=10, pady=12)
            return

        for schedule in schedules:
            row = ctk.CTkFrame(self.schedule_list)
            row.pack(fill="x", padx=5, pady=5)
            row.grid_columnconfigure(0, weight=1)

            details = (
                f"{schedule.query}\n"
                f"Every {schedule.interval_minutes} minutes   "
                f"Sources: {', '.join(schedule.source_names)}"
            )
            ctk.CTkLabel(
                row,
                text=details,
                justify="left",
                anchor="w",
            ).grid(row=0, column=0, sticky="ew", padx=10, pady=10)

            enabled = ctk.BooleanVar(value=schedule.enabled)
            ctk.CTkSwitch(
                row,
                text="Enabled",
                variable=enabled,
                command=lambda item=schedule, value=enabled: self.set_enabled(
                    item.schedule_id,
                    value.get(),
                ),
            ).grid(row=0, column=1, padx=8)

            ctk.CTkButton(
                row,
                text="Run Now",
                width=82,
                command=lambda item=schedule: self.run_now(item.schedule_id),
            ).grid(row=0, column=2, padx=4)

            ctk.CTkButton(
                row,
                text="Delete",
                width=75,
                fg_color="#A33A3A",
                hover_color="#7F2D2D",
                command=lambda item=schedule: self.delete_schedule(item.schedule_id),
            ).grid(row=0, column=3, padx=(4, 10))

    def set_enabled(self, schedule_id, enabled):
        self.scheduler.set_enabled(schedule_id, enabled)
        self.message.configure(text="Schedule updated.")

    def delete_schedule(self, schedule_id):
        self.scheduler.remove(schedule_id)
        self.message.configure(text="Schedule deleted.")
        self.refresh_schedules()

    def run_now(self, schedule_id):
        self.message.configure(text="Running scheduled search...")
        self.master.task_manager.submit(
            name="Run scheduled search now",
            target=self.runner.run_schedule,
            args=(schedule_id,),
            on_success=self.finish_run_now,
            on_error=self.fail_run_now,
        )

    def finish_run_now(self, result):
        if result.succeeded:
            self.message.configure(
                text=f"Scheduled search finished: {result.opportunity_count} result(s)."
            )
        else:
            self.message.configure(text=f"Scheduled search failed: {result.error}")

        self.refresh_schedules()
        self.refresh_history()

    def fail_run_now(self, error):
        self.message.configure(text=f"Scheduled search failed: {error}")

    def refresh_history(self):
        for widget in self.history_list.winfo_children():
            widget.destroy()

        results = self.history_store.load()
        if not results:
            ctk.CTkLabel(
                self.history_list,
                text="No scheduled search results yet.",
                anchor="w",
            ).pack(fill="x", padx=10, pady=12)
            return

        for result in reversed(results[-20:]):
            row = ctk.CTkFrame(self.history_list)
            row.pack(fill="x", padx=5, pady=5)

            if result.succeeded:
                status = f"Completed — {result.opportunity_count} result(s)"
            else:
                status = f"Failed — {result.error}"

            titles = [
                str(item.get("title", "")).strip()
                for item in result.opportunities[:3]
                if str(item.get("title", "")).strip()
            ]
            title_text = "\n".join(f"• {title}" for title in titles)
            details = (
                f"{result.query}\n"
                f"{status}\n"
                f"{result.completed_at}"
            )
            if title_text:
                details = f"{details}\n{title_text}"

            ctk.CTkLabel(
                row,
                text=details,
                justify="left",
                anchor="w",
                wraplength=650,
            ).pack(fill="x", padx=10, pady=9)
