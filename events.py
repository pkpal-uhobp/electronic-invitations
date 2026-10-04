"""Работа с событиями предметной области."""

from datetime import date
from typing import Iterable

from models import Event


def check_event(name: str, event_date: date) -> bool:
    """Проверить корректность названия и даты события."""
    return bool(name.strip()) and event_date >= date.today()


def _next_id(values: Iterable[str]) -> str:
    """Вернуть следующий строковый числовой идентификатор."""
    return str(max((int(value) for value in values), default=0) + 1)


def add_event(events, name: str, event_date: date, user=None):
    """Добавить событие.

    Поддерживается формат ПР2 (словарь) и объектная коллекция ПР3 (список
    объектов Event). Это сохраняет совместимость старых автоматических тестов.
    """
    if not check_event(name, event_date):
        raise ValueError("Некорректные данные события")

    if isinstance(events, dict):
        event_id = _next_id(events.keys())
        events[event_id] = {
            "name": name.strip(),
            "date": event_date.isoformat(),
        }
        return event_id

    event_id = _next_id(event.id for event in events)
    event = Event(event_id, name.strip(), event_date.isoformat(), user)
    events.append(event)
    return event


def find_events(events, query: str):
    """Найти события по части названия."""
    query = query.lower()
    if isinstance(events, dict):
        return [
            (event_id, item)
            for event_id, item in events.items()
            if query in item["name"].lower()
        ]
    return [event for event in events if query in event.name.lower()]


def sort_events(events):
    """Отсортировать события по дате и названию."""
    if isinstance(events, dict):
        return sorted(
            events.items(),
            key=lambda item: (item[1]["date"], item[1]["name"].lower()),
        )
    return sorted(events, key=lambda event: (event.date, event.name.lower()))


def iter_upcoming_events(events):
    """Последовательно вернуть будущие события."""
    today = date.today().isoformat()
    if isinstance(events, dict):
        for event_id, item in sort_events(events):
            if item["date"] >= today:
                yield event_id, item
        return

    for event in sort_events(events):
        if event.date >= today:
            yield event


def find_event_by_id(events: list[Event], event_id: int | str) -> Event | None:
    """Найти объект Event по идентификатору для динамического URL."""
    target = str(event_id)
    for event in events:
        if event.id == target:
            return event
    return None
