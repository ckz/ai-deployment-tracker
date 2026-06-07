"""Load and validate the company watchlist for the tracker MVP."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REQUIRED_FIELDS = ("name", "category", "website", "priority_score", "notes")


def default_companies_path() -> Path:
    return Path(__file__).resolve().parent.parent / "data" / "companies.json"


def load_companies(path: str | Path | None = None) -> list[dict[str, Any]]:
    companies_path = Path(path) if path is not None else default_companies_path()
    with companies_path.open("r", encoding="utf-8") as handle:
        companies = json.load(handle)

    if not isinstance(companies, list):
        raise ValueError("companies.json must contain a list of company records")

    normalized: list[dict[str, Any]] = []
    for index, company in enumerate(companies, start=1):
        if not isinstance(company, dict):
            raise ValueError(f"company record #{index} must be an object")
        missing = [field for field in REQUIRED_FIELDS if field not in company]
        if missing:
            raise ValueError(f"company record #{index} is missing fields: {', '.join(missing)}")
        normalized.append(company)
    return normalized
