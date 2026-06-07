from models import Company, DailySnapshot, EvidenceItem


def test_company_model_fields():
    company = Company(
        name="Modal",
        category="ai_gpu_platform",
        website="https://modal.com",
        priority_score=95,
        notes="Serverless compute",
    )

    assert company.name == "Modal"
    assert company.priority_score == 95


def test_daily_snapshot_model_fields():
    snapshot = DailySnapshot(
        company_name="Modal",
        snapshot_date="2026-06-07",
        score=88,
        summary="Momentum increased",
    )

    assert snapshot.score == 88
    assert snapshot.snapshot_date == "2026-06-07"


def test_evidence_item_model_fields():
    evidence = EvidenceItem(
        company_name="Modal",
        source_url="https://modal.com/docs",
        source_type="docs",
        title="Docs update",
        published_date=None,
        captured_date="2026-06-07",
        quote_or_summary="New feature launched",
        confidence_score=0.9,
    )

    assert evidence.source_type == "docs"
    assert evidence.confidence_score == 0.9
