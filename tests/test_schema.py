from pathlib import Path


def test_schema_contains_required_tables():
    schema = Path("src/schema.sql").read_text(encoding="utf-8")

    assert "CREATE TABLE IF NOT EXISTS companies" in schema
    assert "CREATE TABLE IF NOT EXISTS daily_snapshots" in schema
    assert "CREATE TABLE IF NOT EXISTS evidence" in schema
    assert "CREATE TABLE IF NOT EXISTS weekly_reports" in schema


def test_schema_companies_table_has_required_columns():
    schema = Path("src/schema.sql").read_text(encoding="utf-8")

    for column in ["name", "category", "website", "priority_score", "notes"]:
        assert column in schema
