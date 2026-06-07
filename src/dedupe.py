"""Deduplication helpers for evidence content."""

from __future__ import annotations

from hashlib import sha256


def content_hash(text: str) -> str:
    normalized = " ".join(text.split()).strip().lower()
    return sha256(normalized.encode("utf-8")).hexdigest()


def is_duplicate(text: str, seen_hashes: set[str]) -> bool:
    return content_hash(text) in seen_hashes
