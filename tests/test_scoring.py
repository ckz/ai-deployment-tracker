from scoring import score_company


def test_score_company_returns_bounded_integer():
    score = score_company(
        priority_score=90,
        evidence_texts=[
            "New pricing page launched with GPU support",
            "Enterprise customer case study published",
        ],
    )

    assert isinstance(score, int)
    assert 0 <= score <= 100


def test_score_company_increases_with_strong_signals():
    low = score_company(priority_score=70, evidence_texts=["homepage text only"])
    high = score_company(
        priority_score=70,
        evidence_texts=["new launch pricing gpu enterprise customer model release"],
    )

    assert high > low
