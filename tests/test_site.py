from reports.site import render_index_page


def test_render_index_page_contains_link_and_company_names():
    html = render_index_page(
        "2026-06-07",
        "daily/2026-06-07.md",
        [
            {"name": "Modal", "score": 83, "delta": 0, "summary": "Positive signals", "change_type": "ongoing"},
            {
                "name": "Coolify",
                "score": 51,
                "delta": 0,
                "summary": "No major new signals detected",
                "change_type": "new",
            },
        ],
    )

    assert "AI Deployment Platform Tracker" in html
    assert "daily/2026-06-07.md" in html
    assert "Modal" in html
    assert "Coolify" in html
    assert "ongoing" in html
