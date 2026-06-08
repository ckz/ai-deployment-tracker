from reports.daily import render_daily_report


def test_daily_report_contains_summary_sections():
    report = render_daily_report(
        report_date="2026-06-07",
        rows=[
            {
                "name": "Modal",
                "category": "ai_gpu_platform",
                "score": 97,
                "delta": 4,
                "summary": "New pricing and GPU language detected",
                "change_type": "improved",
                "sources": 3,
            },
            {
                "name": "Railway",
                "category": "developer_cloud",
                "score": 84,
                "delta": -1,
                "summary": "Mostly unchanged",
                "change_type": "ongoing",
                "sources": 3,
            },
        ],
    )

    assert "# Daily Report — 2026-06-07" in report
    assert "## Top Winners" in report
    assert "Modal" in report
    assert "improved" in report
    assert "## Top Losers" in report
    assert "Railway" in report
