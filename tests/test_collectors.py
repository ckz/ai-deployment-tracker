from pathlib import Path
from unittest.mock import Mock, patch

from collectors import collect_company_sources, fetch_text, raw_snapshot_path


def test_fetch_text_strips_html_tags():
    fake_response = Mock()
    fake_response.__enter__ = Mock(return_value=fake_response)
    fake_response.__exit__ = Mock(return_value=False)
    fake_response.read.return_value = b"<html><body><h1>Hello</h1><p>World</p></body></html>"

    with patch("collectors.urlopen", return_value=fake_response):
        text = fetch_text("https://example.com")

    assert text == "Hello World"


def test_raw_snapshot_path_uses_company_and_date():
    path = raw_snapshot_path("data", "Modal", "2026-06-07", "docs")

    assert path == Path("data/raw/modal/2026-06-07/docs.txt")


def test_collect_company_sources_writes_snapshot_files(tmp_path):
    fake_response = Mock()
    fake_response.__enter__ = Mock(return_value=fake_response)
    fake_response.__exit__ = Mock(return_value=False)
    fake_response.read.return_value = b"<html><body>Modal docs</body></html>"

    with patch("collectors.urlopen", return_value=fake_response):
        saved_files = collect_company_sources("Modal", tmp_path, "2026-06-07")

    assert len(saved_files) == 3
    assert (tmp_path / "raw" / "modal" / "2026-06-07" / "homepage.txt").exists()
    assert (tmp_path / "raw" / "modal" / "2026-06-07" / "docs.txt").exists()
    assert (tmp_path / "raw" / "modal" / "2026-06-07" / "pricing.txt").exists()
