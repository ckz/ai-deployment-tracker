from pathlib import Path

from storage import SCHEMA_PATH


def test_schema_contains_expected_tables_and_migration_column():
    schema = SCHEMA_PATH.read_text(encoding="utf-8")
    assert "CREATE TABLE IF NOT EXISTS companies" in schema
    assert "CREATE TABLE IF NOT EXISTS daily_snapshots" in schema
    assert "evidence_signature TEXT" in schema
    assert "CREATE TABLE IF NOT EXISTS evidence" in schema
    assert "CREATE TABLE IF NOT EXISTS weekly_reports" in schema
