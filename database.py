"""
database.py
===========
Lightweight SQLite persistence layer used for logging detection events
and powering the Analytics dashboard. All access is funneled through the
`Database` class so the rest of the app never writes raw SQL.
"""

from __future__ import annotations

import sqlite3
import threading
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime
from typing import Iterator

from config import DB_PATH


@dataclass
class DetectionRecord:
    timestamp: str
    emotion: str
    confidence: float
    song_played: str | None


class Database:
    """Thread-safe SQLite wrapper (one connection per thread)."""

    def __init__(self, db_path=DB_PATH) -> None:
        self.db_path = str(db_path)
        self._local = threading.local()
        self._init_schema()

    # ------------------------------------------------------------------ #
    # Connection handling
    # ------------------------------------------------------------------ #
    @property
    def _conn(self) -> sqlite3.Connection:
        if not hasattr(self._local, "conn"):
            self._local.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self._local.conn.row_factory = sqlite3.Row
        return self._local.conn

    @contextmanager
    def _cursor(self) -> Iterator[sqlite3.Cursor]:
        cur = self._conn.cursor()
        try:
            yield cur
            self._conn.commit()
        finally:
            cur.close()

    def _init_schema(self) -> None:
        with self._cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS detections (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp   TEXT    NOT NULL,
                    emotion     TEXT    NOT NULL,
                    confidence  REAL    NOT NULL,
                    song_played TEXT
                )
                """
            )
            cur.execute(
                "CREATE INDEX IF NOT EXISTS idx_detections_ts ON detections(timestamp)"
            )

    # ------------------------------------------------------------------ #
    # Writes
    # ------------------------------------------------------------------ #
    def log_detection(
        self, emotion: str, confidence: float, song_played: str | None = None
    ) -> None:
        with self._cursor() as cur:
            cur.execute(
                "INSERT INTO detections (timestamp, emotion, confidence, song_played) "
                "VALUES (?, ?, ?, ?)",
                (datetime.now().isoformat(timespec="seconds"), emotion, confidence, song_played),
            )

    def clear_history(self) -> None:
        with self._cursor() as cur:
            cur.execute("DELETE FROM detections")

    # ------------------------------------------------------------------ #
    # Reads
    # ------------------------------------------------------------------ #
    def fetch_all(self, limit: int = 5000) -> list[DetectionRecord]:
        with self._cursor() as cur:
            cur.execute(
                "SELECT timestamp, emotion, confidence, song_played "
                "FROM detections ORDER BY id DESC LIMIT ?",
                (limit,),
            )
            rows = cur.fetchall()
        return [
            DetectionRecord(row["timestamp"], row["emotion"], row["confidence"], row["song_played"])
            for row in rows
        ]

    def total_count(self) -> int:
        with self._cursor() as cur:
            cur.execute("SELECT COUNT(*) AS c FROM detections")
            return int(cur.fetchone()["c"])

    def most_frequent_emotion(self) -> str | None:
        with self._cursor() as cur:
            cur.execute(
                "SELECT emotion, COUNT(*) AS c FROM detections "
                "GROUP BY emotion ORDER BY c DESC LIMIT 1"
            )
            row = cur.fetchone()
        return row["emotion"] if row else None

    def average_confidence(self) -> float:
        with self._cursor() as cur:
            cur.execute("SELECT AVG(confidence) AS avg_c FROM detections")
            row = cur.fetchone()
        return float(row["avg_c"]) if row and row["avg_c"] is not None else 0.0

    def emotion_counts(self) -> dict[str, int]:
        with self._cursor() as cur:
            cur.execute("SELECT emotion, COUNT(*) AS c FROM detections GROUP BY emotion")
            rows = cur.fetchall()
        return {row["emotion"]: row["c"] for row in rows}