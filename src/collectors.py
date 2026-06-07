"""Very small evidence collector utilities for the MVP."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.request import urlopen

from sources import get_company_sources


class _TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        cleaned = data.strip()
        if cleaned:
            self.parts.append(cleaned)

    def text(self) -> str:
        return " ".join(self.parts)


def fetch_text(url: str) -> str:
    with urlopen(url, timeout=20) as response:
        raw = response.read().decode("utf-8", errors="ignore")

    parser = _TextExtractor()
    parser.feed(raw)
    return parser.text().strip()


def raw_snapshot_path(base_dir: str | Path, company_name: str, snapshot_date: str, source_type: str) -> Path:
    safe_company = company_name.lower().replace(" ", "-")
    safe_source = source_type.lower().replace(" ", "-")
    return Path(base_dir) / "raw" / safe_company / snapshot_date / f"{safe_source}.txt"


def collect_company_sources(company_name: str, base_dir: str | Path, snapshot_date: str) -> list[Path]:
    saved_files: list[Path] = []
    for source in get_company_sources(company_name):
        text = fetch_text(source["url"])
        output_path = raw_snapshot_path(base_dir, company_name, snapshot_date, source["type"])
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(text, encoding="utf-8")
        saved_files.append(output_path)
    return saved_files
