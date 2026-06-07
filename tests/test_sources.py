from sources import COMPANY_SOURCES, get_company_sources


def test_sources_include_all_mvp_companies():
    assert len(COMPANY_SOURCES) == 10


def test_modal_has_homepage_docs_and_pricing():
    source_types = {source["type"] for source in get_company_sources("Modal")}

    assert source_types == {"homepage", "docs", "pricing"}
