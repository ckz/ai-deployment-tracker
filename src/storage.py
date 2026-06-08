"""SQLite storage helpers for the tracker MVP."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

from dedupe import content_hash

SCHEMA_PATH = Path(__file__).resolve().parent / "schema.sql"


def _connect(db_path: str | Path) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: str | Path) -> None:
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    schema = SCHEMA_PATH.read_text(encoding="utf-8")
    with _connect(db_path) as conn:
        conn.executescript(schema)
        existing_columns = {
            row["name"]
            for row in conn.execute("PRAGMA table_info(daily_snapshots)").fetchall()
        }
        if "evidence_signature" not in existing_columns:
            conn.execute("ALTER TABLE daily_snapshots ADD COLUMN evidence_signature TEXT")
        conn.commit()


def upsert_company(db_path: str | Path, company: dict[str, Any]) -> int:
    with _connect(db_path) as conn:
        row = conn.execute("SELECT id FROM companies WHERE name = ?", (company["name"],)).fetchone()
        if row:
            conn.execute(
                """
                UPDATE companies
                SET category = ?, website = ?, priority_score = ?, notes = ?
                WHERE id = ?
                """,
                (company["category"], company["website"], company["priority_score"], company["notes"], row["id"]),
            )
            conn.commit()
            return int(row["id"])

        cursor = conn.execute(
            """
            INSERT INTO companies (name, category, website, priority_score, notes)
            VALUES (?, ?, ?, ?, ?)
            """,
            (company["name"], company["category"], company["website"], company["priority_score"], company["notes"]),
        )
        conn.commit()
        return int(cursor.lastrowid)


def upsert_evidence(db_path: str | Path, evidence: dict[str, Any]) -> int:
    with _connect(db_path) as conn:
        row = conn.execute(
            "SELECT id FROM evidence WHERE company_id = ? AND content_hash = ?",
            (evidence["company_id"], evidence["content_hash"]),
        ).fetchone()
        if row:
            return int(row["id"])

        cursor = conn.execute(
            """
            INSERT INTO evidence (
                company_id, source_url, source_type, title,
                published_date, captured_date, quote_or_summary,
                confidence_score, content_hash
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                evidence["company_id"],
                evidence["source_url"],
                evidence["source_type"],
                evidence["title"],
                evidence["published_date"],
                evidence["captured_date"],
                evidence["quote_or_summary"],
                evidence["confidence_score"],
                evidence["content_hash"],
            ),
        )
        conn.commit()
        return int(cursor.lastrowid)


def upsert_snapshot(db_path: str | Path, snapshot: dict[str, Any]) -> int:
    with _connect(db_path) as conn:
        row = conn.execute(
            "SELECT id FROM daily_snapshots WHERE company_id = ? AND snapshot_date = ?",
            (snapshot["company_id"], snapshot["snapshot_date"]),
        ).fetchone()
        if row:
            conn.execute(
                "UPDATE daily_snapshots SET score = ?, summary = ?, evidence_signature = ? WHERE id = ?",
                (snapshot["score"], snapshot["summary"], snapshot.get("evidence_signature"), row["id"]),
            )
            conn.commit()
            return int(row["id"])

        cursor = conn.execute(
            """
            INSERT INTO daily_snapshots (company_id, snapshot_date, score, summary, evidence_signature)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                snapshot["company_id"],
                snapshot["snapshot_date"],
                snapshot["score"],
                snapshot["summary"],
                snapshot.get("evidence_signature"),
            ),
        )
        conn.commit()
        return int(cursor.lastrowid)


def get_latest_snapshot(db_path: str | Path, company_id: int) -> dict[str, Any] | None:
    with _connect(db_path) as conn:
        row = conn.execute(
            """
            SELECT company_id, snapshot_date, score, summary, evidence_signature
            FROM daily_snapshots
            WHERE company_id = ?
            ORDER BY snapshot_date DESC, id DESC
            LIMIT 1
            """,
            (company_id,),
        ).fetchone()
        return dict(row) if row else None


def get_previous_snapshot(db_path: str | Path, company_id: int, snapshot_date: str) -> dict[str, Any] | None:
    with _connect(db_path) as conn:
        row = conn.execute(
            """
            SELECT company_id, snapshot_date, score, summary, evidence_signature
            FROM daily_snapshots
            WHERE company_id = ? AND snapshot_date < ?
            ORDER BY snapshot_date DESC, id DESC
            LIMIT 1
            """,
            (company_id, snapshot_date),
        ).fetchone()
        return dict(row) if row else None


def get_company_rows(db_path: str | Path) -> list[dict[str, Any]]:
    with _connect(db_path) as conn:
        rows = conn.execute(
            "SELECT id, name, category, website, priority_score, notes FROM companies ORDER BY priority_score DESC, name ASC"
        ).fetchall()
        return [dict(row) for row in rows]


def get_company_by_name(db_path: str | Path, name: str) -> dict[str, Any] | None:
    with _connect(db_path) as conn:
        row = conn.execute(
            "SELECT id, name, category, website, priority_score, notes FROM companies WHERE name = ?",
            (name,),
        ).fetchone()
        return dict(row) if row else None
