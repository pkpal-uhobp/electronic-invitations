"""ПР7: события из SQLite, фильтрация даты и поиск не приглашённых гостей."""
from datetime import date
from django.http import Http404
from django.shortcuts import render
from db import queries, repository


def events(request):
    return render(request, 'events_web/event_list.html', {
        'page_title': 'События', 'events': repository.events(),
    })


def event_detail(request, event_id: int):
    row = queries.one('event_by_id', (event_id,))
    if row is None:
        raise Http404('Событие не найдено')
    event = repository.event_from_row(row)
    event_date = date.fromisoformat(event.date)
    return render(request, 'events_web/event_detail.html', {
        'page_title': event.name, 'event': event, 'event_date': event_date,
        'is_upcoming': event_date >= date.today(),
    })


def search_by_date(request):
    """WHERE с параметром из пользовательской GET-формы."""
    selected_date = request.GET.get('date', '').strip()
    found = []
    error = ''
    if selected_date:
        try:
            parsed = date.fromisoformat(selected_date)
            if parsed.isoformat() != selected_date:
                raise ValueError('Формат даты')
            found = repository.events('events_on_date', (selected_date,))
        except ValueError:
            error = 'Укажите дату в формате ГГГГ-ММ-ДД.'
    return render(request, 'events_web/event_search.html', {
        'page_title': 'Поиск по дате', 'events': found, 'selected_date': selected_date,
        'has_searched': bool(selected_date and not error), 'error': error,
    })


def available_guests(request):
    """Аналог задачи ПР7 по свободным помещениям: не приглашённые на событие гости."""
    selected_id_text = request.GET.get('event_id', '').strip()
    selected_id = None
    available = []
    error = ''
    if selected_id_text:
        try:
            selected_id = int(selected_id_text)
        except ValueError:
            error = 'Выберите событие из списка.'
        else:
            if queries.one('event_by_id', (selected_id,)) is None:
                error = 'Событие не найдено.'
            else:
                available = queries.rows('available_guests', (selected_id,))
    return render(request, 'events_web/available_guests.html', {
        'page_title': 'Свободные гости', 'events': repository.events(),
        'available': available, 'selected_id': selected_id,
        'searched': bool(selected_id_text and not error), 'error': error,
    })
