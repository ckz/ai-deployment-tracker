"""Markdown report generation for the daily tracker output."""

from __future__ import annotations


def render_daily_report(report_date: str, rows: list[dict]) -> str:
    winners = [row for row in rows if row["delta"] > 0]
    losers = [row for row in rows if row["delta"] < 0]
    new_items = [row for row in rows if row.get("change_type") == "new"]
    improved_items = [row for row in rows if row.get("change_type") == "improved"]
    ongoing_items = [row for row in rows if row.get("change_type") == "ongoing"]
    flat = sorted(rows, key=lambda row: (-row["delta"], -row["score"], row["name"]))

    lines: list[str] = [f"# Daily Report — {report_date}", ""]
    lines.extend(["## Overview", ""])
    lines.append(f"- Companies tracked: {len(rows)}")
    lines.append(f"- Rising today: {len(winners)}")
    lines.append(f"- Falling today: {len(losers)}")
    lines.append(f"- New signals: {len(new_items)}")
    lines.append(f"- Improved signals: {len(improved_items)}")
    lines.append(f"- Ongoing signals: {len(ongoing_items)}")
    lines.append("")

    lines.extend(["## Top Winners", ""])
    if winners:
        for row in sorted(winners, key=lambda row: (-row["delta"], -row["score"], row["name"])):
            lines.append(
                f"- **{row['name']}** — score {row['score']} ({row['delta']:+d}) — {row.get('change_type', 'ongoing')} — {row['summary']}"
            )
    else:
        lines.append("- No notable winners today.")
    lines.append("")

    lines.extend(["## Top Losers", ""])
    if losers:
        for row in sorted(losers, key=lambda row: (row["delta"], row["score"], row["name"])):
            lines.append(
                f"- **{row['name']}** — score {row['score']} ({row['delta']:+d}) — {row.get('change_type', 'ongoing')} — {row['summary']}"
            )
    else:
        lines.append("- No notable losers today.")
    lines.append("")

    lines.extend(["## All Companies", ""])
    for row in flat:
        lines.append(
            f"- {row['name']} — score {row['score']} ({row['delta']:+d}) — {row.get('change_type', 'ongoing')} — {row['sources']} sources — {row['summary']}"
        )

    lines.append("")
    return "\n".join(lines)
