from pathlib import Path

from storage import load_json, save_json


def test_json_round_trip(tmp_path: Path) -> None:
    path = tmp_path / "data.json"
    expected = {"1": {"name": "Событие", "date": "2026-10-15"}}

    save_json(path, expected)
    actual = load_json(path, {})

    assert actual == expected
