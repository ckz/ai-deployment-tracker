from dedupe import content_hash, is_duplicate


def test_content_hash_changes_with_content():
    assert content_hash("hello") != content_hash("hello world")


def test_is_duplicate_detects_existing_hash():
    seen = {content_hash("hello")}
    assert is_duplicate("hello", seen) is True
    assert is_duplicate("world", seen) is False
