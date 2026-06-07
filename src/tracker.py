"""Entry point for the AI Deployment Platform Tracker MVP."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

from collectors import collect_company_sources
from company_registry import default_companies_path, load_companies
from dedupe import content_hash
from reports.daily import render_daily_report
from reports.site import render_index_page
from scoring import score_company
from sources import get_company_sources
from storage import (
    get_previous_snapshot,
    init_db,
    upsert_company,
    upsert_evidence,
    upsert_snapshot,
)

REPORT_DIR = Path("reports")
DEFAULT_DB_PATH = Path("data") / "tracker.db"
DEFAULT_DATA_DIR = Path("data")


POSITIVE_SIGNAL_KEYWORDS = (
    "launch",
    "released",
    "release",
    "pricing",
    "gpu",
    "model",
    "gateway",
    "enterprise",
    "customer",
    "customers",
    "partner",
    "partnership",
    "beta",
    "docs",
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="AI Deployment Platform Tracker")
    parser.add_argument(
        "--companies",
        type=Path,
        default=default_companies_path(),
        help="Path to the companies registry JSON file.",
    )
    parser.add_argument(
        "--db",
        type=Path,
        default=DEFAULT_DB_PATH,
        help="Path to the local SQLite database.",
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=DEFAULT_DATA_DIR,
        help="Base directory for raw evidence snapshots.",
    )
    parser.add_argument(
        "--report-dir",
        type=Path,
        default=REPORT_DIR,
        help="Directory for generated daily reports.",
    )
    return parser


def summarize_texts(texts: list[str]) -> str:
    blob = " ".join(texts).lower()
    hits = [keyword for keyword in POSITIVE_SIGNAL_KEYWORDS if keyword in blob]
    if not hits:
        return "No major new signals detected"
    return f"Positive signals: {', '.join(hits[:5])}"


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    companies = load_companies(args.companies)
    today = date.today().isoformat()

    init_db(args.db)

    for company in companies:
        upsert_company(args.db, company)

    report_rows: list[dict] = []

    for company in companies:
        company_id = upsert_company(args.db, company)
        company_sources = get_company_sources(company["name"])
        snapshot_paths = collect_company_sources(company["name"], args.data_dir, today)
        evidence_texts: list[str] = []
        source_count = len(snapshot_paths)
        new_evidence_count = 0

        for source, path in zip(company_sources, snapshot_paths):
            text = path.read_text(encoding="utf-8")
            evidence_texts.append(text)
            if text.startswith("ERROR fetching"):
                continue

            evidence_hash = content_hash(text)
            upsert_evidence(
                args.db,
                {
                    "company_id": company_id,
                    "source_url": source["url"],
                    "source_type": source["type"],
                    "title": f"{company['name']} {source['type']}",
                    "published_date": None,
                    "captured_date": today,
                    "quote_or_summary": text[:500],
                    "confidence_score": 0.75,
                    "content_hash": evidence_hash,
                },
            )
            new_evidence_count += 1

        score = score_company(company["priority_score"], evidence_texts)
        previous = get_previous_snapshot(args.db, company_id, today)
        delta = score - previous["score"] if previous else 0
        summary = summarize_texts(evidence_texts)

        upsert_snapshot(
            args.db,
            {
                "company_id": company_id,
                "snapshot_date": today,
                "score": score,
                "summary": summary,
            },
        )

        report_rows.append(
            {
                "name": company["name"],
                "category": company["category"],
                "score": score,
                "delta": delta,
                "summary": summary,
                "sources": source_count,
                "new_evidence": new_evidence_count,
            }
        )

    args.report_dir.mkdir(parents=True, exist_ok=True)
    daily_dir = args.report_dir / "daily"
    daily_dir.mkdir(parents=True, exist_ok=True)
    report_path = daily_dir / f"{today}.md"
    report_path.write_text(render_daily_report(today, report_rows), encoding="utf-8")

    index_path = args.report_dir / "index.html"
    index_path.write_text(
        render_index_page(today, f"daily/{report_path.name}", report_rows),
        encoding="utf-8",
    )

    print(f"Loaded {len(companies)} companies from {args.companies}")
    print(f"Wrote daily report to {report_path}")
    for row in sorted(report_rows, key=lambda item: (-item["delta"], -item["score"], item["name"])):
        print(f"- {row['name']}: {row['score']} ({row['delta']:+d})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
