"""
OpportunityLab Search History Service

Stores and retrieves recent search queries using SQLite.
"""

import sqlite3
from datetime import datetime
from pathlib import Path


class SearchHistoryService:

    def __init__(
        self,
        db_path="data/opportunities.db",
        maximum_history=100
    ):

        self.db_path = Path(db_path)
        self.maximum_history = maximum_history

        self.db_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.initialize()

    def initialize(self):

        with sqlite3.connect(self.db_path) as connection:

            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS search_history
                (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    query TEXT NOT NULL UNIQUE COLLATE NOCASE,
                    search_count INTEGER NOT NULL DEFAULT 1,
                    first_searched_at TEXT NOT NULL,
                    last_searched_at TEXT NOT NULL
                )
                """
            )

            connection.commit()

    def add_search(self, query):

        query = self.normalize_query(query)

        if not query:
            return False

        now = datetime.now().isoformat(
            timespec="seconds"
        )

        with sqlite3.connect(self.db_path) as connection:

            connection.execute(
                """
                INSERT INTO search_history
                (
                    query,
                    search_count,
                    first_searched_at,
                    last_searched_at
                )
                VALUES (?, 1, ?, ?)

                ON CONFLICT(query)
                DO UPDATE SET
                    search_count = search_count + 1,
                    last_searched_at = excluded.last_searched_at
                """,
                (
                    query,
                    now,
                    now
                )
            )

            connection.commit()

        self.trim_history()

        return True

    def get_recent_searches(self, limit=10):

        limit = self.clean_limit(limit)

        with sqlite3.connect(self.db_path) as connection:

            cursor = connection.execute(
                """
                SELECT query
                FROM search_history
                ORDER BY last_searched_at DESC
                LIMIT ?
                """,
                (limit,)
            )

            rows = cursor.fetchall()

        return [
            row[0]
            for row in rows
        ]

    def get_suggestions(
        self,
        text,
        limit=8
    ):

        text = self.normalize_query(text)
        limit = self.clean_limit(limit)

        if not text:
            return self.get_recent_searches(limit)

        starts_with = f"{text}%"
        contains = f"%{text}%"

        with sqlite3.connect(self.db_path) as connection:

            cursor = connection.execute(
                """
                SELECT query
                FROM search_history
                WHERE query LIKE ? COLLATE NOCASE
                   OR query LIKE ? COLLATE NOCASE
                ORDER BY
                    CASE
                        WHEN query LIKE ? COLLATE NOCASE
                        THEN 0
                        ELSE 1
                    END,
                    search_count DESC,
                    last_searched_at DESC
                LIMIT ?
                """,
                (
                    starts_with,
                    contains,
                    starts_with,
                    limit
                )
            )

            rows = cursor.fetchall()

        return [
            row[0]
            for row in rows
        ]

    def remove_search(self, query):

        query = self.normalize_query(query)

        if not query:
            return False

        with sqlite3.connect(self.db_path) as connection:

            cursor = connection.execute(
                """
                DELETE FROM search_history
                WHERE query = ? COLLATE NOCASE
                """,
                (query,)
            )

            connection.commit()

            return cursor.rowcount > 0

    def clear_history(self):

        with sqlite3.connect(self.db_path) as connection:

            connection.execute(
                "DELETE FROM search_history"
            )

            connection.commit()

    def trim_history(self):

        with sqlite3.connect(self.db_path) as connection:

            connection.execute(
                """
                DELETE FROM search_history
                WHERE id NOT IN
                (
                    SELECT id
                    FROM search_history
                    ORDER BY last_searched_at DESC
                    LIMIT ?
                )
                """,
                (self.maximum_history,)
            )

            connection.commit()

    def normalize_query(self, query):

        return " ".join(
            str(query).strip().split()
        )

    def clean_limit(self, limit):

        try:
            limit = int(limit)

        except (TypeError, ValueError):
            limit = 10

        return max(
            1,
            min(limit, 50)
        )