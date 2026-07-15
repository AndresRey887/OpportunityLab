"""
Persistent AI Analysis Cache

Stores structured OpportunityAnalysis results in SQLite.
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path

from src.ai.opportunity_analysis import OpportunityAnalysis


class AnalysisCache:

    def __init__(self, db_path="data/opportunities.db"):

        self.db_path = Path(db_path)

        self.db_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.initialize()

    def initialize(self):

        with sqlite3.connect(self.db_path) as connection:

            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS ai_analysis_cache
                (
                    cache_key TEXT PRIMARY KEY,
                    opportunity_url TEXT,
                    opportunity_title TEXT,
                    analysis_json TEXT NOT NULL,
                    provider_name TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )

            connection.commit()

    def get(self, cache_key):

        if not cache_key:
            return None

        with sqlite3.connect(self.db_path) as connection:

            cursor = connection.execute(
                """
                SELECT analysis_json
                FROM ai_analysis_cache
                WHERE cache_key = ?
                """,
                (cache_key,)
            )

            row = cursor.fetchone()

        if row is None:
            return None

        try:

            data = json.loads(row[0])

            return OpportunityAnalysis.from_dict(data)

        except (json.JSONDecodeError, TypeError, ValueError):

            return None

    def save(
        self,
        cache_key,
        opportunity,
        analysis,
        provider_name=""
    ):

        if not cache_key:
            return False

        if not isinstance(analysis, OpportunityAnalysis):
            return False

        now = datetime.now().isoformat(
            timespec="seconds"
        )

        analysis_json = json.dumps(
            analysis.to_dict(),
            ensure_ascii=False
        )

        with sqlite3.connect(self.db_path) as connection:

            connection.execute(
                """
                INSERT INTO ai_analysis_cache
                (
                    cache_key,
                    opportunity_url,
                    opportunity_title,
                    analysis_json,
                    provider_name,
                    created_at,
                    updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)

                ON CONFLICT(cache_key)
                DO UPDATE SET
                    opportunity_url = excluded.opportunity_url,
                    opportunity_title = excluded.opportunity_title,
                    analysis_json = excluded.analysis_json,
                    provider_name = excluded.provider_name,
                    updated_at = excluded.updated_at
                """,
                (
                    cache_key,
                    str(
                        getattr(
                            opportunity,
                            "url",
                            ""
                        )
                    ),
                    str(
                        getattr(
                            opportunity,
                            "title",
                            ""
                        )
                    ),
                    analysis_json,
                    provider_name,
                    now,
                    now
                )
            )

            connection.commit()

        return True

    def remove(self, cache_key):

        if not cache_key:
            return False

        with sqlite3.connect(self.db_path) as connection:

            cursor = connection.execute(
                """
                DELETE FROM ai_analysis_cache
                WHERE cache_key = ?
                """,
                (cache_key,)
            )

            connection.commit()

            return cursor.rowcount > 0

    def clear(self):

        with sqlite3.connect(self.db_path) as connection:

            connection.execute(
                "DELETE FROM ai_analysis_cache"
            )

            connection.commit()