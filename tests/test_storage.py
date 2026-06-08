from storage import get_latest_snapshot, init_db, upsert_company, upsert_evidence, upsert_snapshot


def test_storage_round_trip(tmp_path):
    db_path = tmp_path / "tracker.db"
    init_db(db_path)

    company_id = upsert_company(
        db_path,
        {
            "name": "Modal",
            "category": "ai_gpu_platform",
            "website": "https://modal.com",
            "priority_score": 95,
            "notes": "Serverless compute",
        },
    )
    evidence_id = upsert_evidence(
        db_path,
        {
            "company_id": company_id,
            "source_url": "https://modal.com/pricing",
            "source_type": "pricing",
            "title": "Pricing",
            "published_date": None,
            "captured_date": "2026-06-07",
            "quote_or_summary": "New pricing page",
            "confidence_score": 0.9,
            "content_hash": "abc123",
        },
    )
    snapshot_id = upsert_snapshot(
        db_path,
        {
            "company_id": company_id,
            "snapshot_date": "2026-06-07",
            "score": 97,
            "summary": "Strong momentum",
            "evidence_signature": "sig-123",
        },
    )

    latest = get_latest_snapshot(db_path, company_id)

    assert evidence_id > 0
    assert snapshot_id > 0
    assert latest is not None
    assert latest["score"] == 97
    assert latest["summary"] == "Strong momentum"
    assert latest["evidence_signature"] == "sig-123"
