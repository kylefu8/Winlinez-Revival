from pathlib import Path

from winlinez.records import HighScoreStore


def test_high_score_store_round_trips_score(tmp_path: Path) -> None:
    store = HighScoreStore()
    store.path = tmp_path / "score.json"

    store.save(125)

    assert store.load() == 125


def test_high_score_store_ignores_missing_or_bad_file(tmp_path: Path) -> None:
    store = HighScoreStore()
    store.path = tmp_path / "missing.json"
    assert store.load() == 0

    store.path.write_text("{not-json", encoding="utf-8")
    assert store.load() == 0
