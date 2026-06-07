"""Entry point for the AI Deployment Platform Tracker MVP."""

from __future__ import annotations

import argparse
from pathlib import Path

from company_registry import default_companies_path, load_companies


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="AI Deployment Platform Tracker")
    parser.add_argument(
        "--companies",
        type=Path,
        default=default_companies_path(),
        help="Path to the companies registry JSON file.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    companies = load_companies(args.companies)
    print(f"Loaded {len(companies)} companies from {args.companies}")
    for company in companies:
        print(f"- {company['name']} ({company['category']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
