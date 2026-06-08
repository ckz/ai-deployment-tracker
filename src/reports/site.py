"""Static site generation for GitHub Pages output."""

from __future__ import annotations

from html import escape


def render_index_page(report_date: str, report_relpath: str, rows: list[dict]) -> str:
    rows = sorted(rows, key=lambda row: (-row["score"], row["name"]))
    items = "\n".join(
        f"<li><strong>{escape(row['name'])}</strong> — score {row['score']} ({row['delta']:+d}) — {escape(row.get('change_type', 'ongoing'))} — {escape(row['summary'])}</li>"
        for row in rows
    )
    return f"""<!doctype html>
<html lang=\"en\">
  <head>
    <meta charset=\"utf-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
    <title>AI Deployment Platform Tracker</title>
    <style>
      body {{ font-family: system-ui, sans-serif; max-width: 900px; margin: 40px auto; padding: 0 20px; line-height: 1.5; }}
      code {{ background: #f4f4f4; padding: 0.2rem 0.4rem; border-radius: 4px; }}
    </style>
  </head>
  <body>
    <h1>AI Deployment Platform Tracker</h1>
    <p>Latest report date: <strong>{escape(report_date)}</strong></p>
    <p><a href=\"{escape(report_relpath)}\">Open daily report</a></p>
    <h2>Current ranking</h2>
    <ul>
      {items}
    </ul>
  </body>
</html>
"""
