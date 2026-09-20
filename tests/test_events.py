from datetime import date, timedelta

import pytest

from events import add_event, check_event, find_events, sort_events


def test_check_event_rejects_empty_name() -> None:
    assert not check_event("", date.today())


def test_add_event_and_find_event() -> None:
    events: dict[str, dict[str, str]] = {}
    future_date = date.today() + timedelta(days=2)

    event_id = add_event(events, "День рождения", future_date)
    result = find_events(events, "рожд")

    assert event_id == "1"
    assert result[0][1]["name"] == "День рождения"


def test_sort_events_by_date() -> None:
    events = {
        "1": {"name": "Позже", "date": "2026-12-10"},
        "2": {"name": "Раньше", "date": "2026-10-10"},
    }

    result = sort_events(events)

    assert [item[0] for item in result] == ["2", "1"]


def test_add_event_rejects_past_date() -> None:
    events: dict[str, dict[str, str]] = {}
    past_date = date.today() - timedelta(days=1)

    with pytest.raises(ValueError):
        add_event(events, "Старое событие", past_date)
