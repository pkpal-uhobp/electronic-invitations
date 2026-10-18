"""События: получение JSON-объектов, контекст и render()."""
from datetime import date
from django.http import Http404
from django.shortcuts import render
from events import find_event_by_id, sort_events
from storage import load_events


def events(request):
    event_list = sort_events(load_events())
    return render(request, 'events_web/event_list.html', {
        'page_title': 'События', 'events': event_list,
    })


def event_detail(request, event_id: int):
    event = find_event_by_id(load_events(), event_id)
    if event is None:
        raise Http404('Событие не найдено')
    event_date = date.fromisoformat(event.date)
    return render(request, 'events_web/event_detail.html', {
        'page_title': event.name, 'event': event, 'event_date': event_date,
        'is_upcoming': event_date >= date.today(),
    })
