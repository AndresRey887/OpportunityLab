"""
Simple logging utility for OpportunityLab
"""

from datetime import datetime


class Logger:
    def info(self, message: str):
        print(f"[INFO] {self._time()} {message}")

    def warning(self, message: str):
        print(f"[WARNING] {self._time()} {message}")

    def error(self, message: str):
        print(f"[ERROR] {self._time()} {message}")

    def _time(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")