"""Simple momentum scoring for the tracker MVP."""

from __future__ import annotations

KEYWORD_WEIGHTS = {
    "launch": 4,
    "released": 4,
    "release": 3,
    "new": 1,
    "pricing": 4,
    "gpu": 5,
    "model": 3,
    "gateway": 4,
    "enterprise": 4,
    "customer": 4,
    "customers": 4,
    "partner": 3,
    "partnership": 4,
    "docs": 1,
    "beta": 2,
    "api": 1,
}


def score_company(priority_score: int, evidence_texts: list[str]) -> int:
    score = int(priority_score * 0.55)
    blob = " ".join(evidence_texts).lower()
    for keyword, weight in KEYWORD_WEIGHTS.items():
        if keyword in blob:
            score += weight
    return max(0, min(100, int(score)))
