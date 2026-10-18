"""Консольная предметная логика событий ПР2–ПР5."""
from datetime import date
from models import Event

def check_event(name: str, event_date: date) -> bool:
    return bool(name.strip()) and event_date >= date.today()

def _next_id(values):
    return str(max((int(value) for value in values), default=0) + 1)

def add_event(events, name: str, event_date: date, user=None):
    if not check_event(name, event_date):
        raise ValueError("Некорректные данные события")
    if isinstance(events, dict):
        event_id = _next_id(events.keys())
        events[event_id] = {"name": name.strip(), "date": event_date.isoformat()}
        return event_id
    event_id = _next_id(e.id for e in events)
    event = Event(event_id, name.strip(), event_date.isoformat(), user)
    events.append(event)
    return event

def find_events(events, query: str):
    query = query.lower()
    if isinstance(events, dict):
        return [(ident, e) for ident, e in events.items() if query in e['name'].lower()]
    return [e for e in events if query in e.name.lower()]

def sort_events(events):
    if isinstance(events, dict):
        return sorted(events.items(), key=lambda i: (i[1]['date'], i[1]['name'].lower()))
    return sorted(events, key=lambda e: (e.date, e.name.lower()))

def iter_upcoming_events(events):
    today = date.today().isoformat()
    if isinstance(events, dict):
        for ident, item in sort_events(events):
            if item['date'] >= today:
                yield ident, item
        return
    for event in sort_events(events):
        if event.date >= today:
            yield event

def find_event_by_id(events, event_id):
    return next((e for e in events if e.id == str(event_id)), None)
