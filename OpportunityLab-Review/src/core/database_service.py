"""
Database Service for OpportunityLab
Handles persistent storage using SQLite.
"""

import sqlite3
from src.core.service import Service


class DatabaseService(Service):

    def __init__(self, db_path="data/opportunities.db"):
        super().__init__("DatabaseService")
        self.db_path = db_path
        self.conn = None

    def initialize(self):
        """Open the database and create tables if required."""

        print("[DB] initialize() CALLED")

        self.conn = sqlite3.connect(self.db_path)

        cursor = self.conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS opportunities (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                title TEXT,
                url TEXT,
                snippet TEXT,
                source TEXT,
                score INTEGER

            )
        """)

        self.conn.commit()

        print("[DB] table creation complete")

    def start(self):
        """Start the database service."""

        super().start()

        print("[DB] Database service started")

    def save_opportunity(self, opportunity):
        """Save an opportunity if it doesn't already exist."""

        cursor = self.conn.cursor()

        # Duplicate check
        cursor.execute(
            "SELECT id FROM opportunities WHERE url = ?",
            (opportunity.url,)
        )

        if cursor.fetchone():
            print(f"[DB] Skipped (already exists): {opportunity.title}")
            return False

        cursor.execute(
            """
            INSERT INTO opportunities
            (
                title,
                url,
                snippet,
                source,
                score
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                opportunity.title,
                opportunity.url,
                opportunity.snippet,
                opportunity.source,
                opportunity.score
            )
        )

        self.conn.commit()

        print(f"[DB] Saved: {opportunity.title}")

        return True

    def stop(self):
        """Close the database."""

        if self.conn:
            self.conn.close()

        super().stop()

        print("[DB] Database connection closed")