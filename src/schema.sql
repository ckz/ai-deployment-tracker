-- Schema for the AI Deployment Platform Tracker MVP

CREATE TABLE IF NOT EXISTS companies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    category TEXT NOT NULL,
    website TEXT NOT NULL,
    priority_score INTEGER NOT NULL,
    notes TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS daily_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    snapshot_date TEXT NOT NULL,
    score INTEGER NOT NULL,
    summary TEXT NOT NULL,
    FOREIGN KEY (company_id) REFERENCES companies(id)
);

CREATE TABLE IF NOT EXISTS evidence (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,
    source_url TEXT NOT NULL,
    source_type TEXT NOT NULL,
    title TEXT NOT NULL,
    published_date TEXT,
    captured_date TEXT NOT NULL,
    quote_or_summary TEXT NOT NULL,
    confidence_score REAL NOT NULL,
    FOREIGN KEY (company_id) REFERENCES companies(id)
);

CREATE TABLE IF NOT EXISTS weekly_reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    week_start TEXT NOT NULL UNIQUE,
    key_winners TEXT NOT NULL,
    key_losers TEXT NOT NULL,
    new_companies TEXT NOT NULL,
    recommendation TEXT NOT NULL
);
