
"""Работа с объектами событий."""
from datetime import date
from models import Event

def add_event(
    events: list[Event],
    name: str,
    event_date: date
) -> Event:

    if not name.strip() or event_date < date.today():
        raise ValueError("Некорректные данные события")

    event_id = str(max((int(e.id) for e in events), default=0) + 1)

    event = Event(
        event_id,
        name.strip(),
        event_date.isoformat()
    )

    events.append(event)

    return event

def find_events(events: list[Event], query: str) -> list[Event]:
    return [e for e in events if query.lower() in e.name.lower()]

def sort_events(events: list[Event]) -> list[Event]:
    return sorted(events, key=lambda e: (e.date, e.name.lower()))

def iter_upcoming_events(events: list[Event]):
    today=date.today().isoformat()
    for e in sort_events(events):
        if e.date >= today:
            yield e
