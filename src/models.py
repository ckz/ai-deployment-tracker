"""Simple data structures for the tracker MVP."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Company:
    name: str
    category: str
    website: str
    priority_score: int
    notes: str


@dataclass(frozen=True)
class DailySnapshot:
    company_name: str
    snapshot_date: str
    score: int
    summary: str


@dataclass(frozen=True)
class EvidenceItem:
    company_name: str
    source_url: str
    source_type: str
    title: str
    published_date: str | None
    captured_date: str
    quote_or_summary: str
    confidence_score: float
