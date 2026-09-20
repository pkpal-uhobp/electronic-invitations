"""Functions for working with events."""

from datetime import date
from typing import Iterator


Events = dict[str, dict[str, str]]
EventItem = tuple[str, dict[str, str]]


def check_event(name: str, event_date: date) -> bool:
    """Check that an event has a name and is not in the past."""
    if not name.strip():
        return False
    return event_date >= date.today()


def add_event(events: Events, name: str, event_date: date) -> str:
    """Add an event to the collection and return its identifier."""
    if not check_event(name, event_date):
        raise ValueError("Некорректные данные события")

    event_id = str(max((int(key) for key in events), default=0) + 1)
    events[event_id] = {
        "name": name.strip(),
        "date": event_date.isoformat(),
    }
    return event_id


def find_events(events: Events, query: str) -> list[EventItem]:
    """Find events whose names contain the query string."""
    normalized_query = query.strip().lower()
    return [
        (event_id, event)
        for event_id, event in events.items()
        if normalized_query in event["name"].lower()
    ]


def sort_events(events: Events) -> list[EventItem]:
    """Return events sorted by date and then by name."""
    return sorted(
        events.items(),
        key=lambda item: (item[1]["date"], item[1]["name"].lower()),
    )


def iter_upcoming_events(events: Events) -> Iterator[EventItem]:
    """Yield events whose date is today or later."""
    today = date.today().isoformat()
    for event_id, event in sort_events(events):
        if event["date"] >= today:
            yield event_id, event
