"""Existing event scenarios, implemented with ORM instead of raw SQL."""
from datetime import date

from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from guests_web.models import Guest
from invitations_web.models import Invitation
from .models import Event

EVENT_SORTS = {'date': 'date', 'name': 'name', 'organizer': 'user__name',
               'date_desc': '-date'}


def events(request):
    query = request.GET.get('q', '').strip()[:100]
    sort = request.GET.get('sort', 'date')
    qs = Event.objects.select_related('user')
    if query:
        qs = qs.filter(Q(name__icontains=query) | Q(user__name__icontains=query))
    qs = qs.order_by(EVENT_SORTS.get(sort, 'date'), 'pk')
    return render(request, 'events_web/event_list.html', {
        'page_title': 'События', 'events': qs, 'query': query, 'selected_sort': sort,
    })


def event_detail(request, event_id: int):
    event = get_object_or_404(Event.objects.select_related('user'), pk=event_id)
    return render(request, 'events_web/event_detail.html', {
        'page_title': event.name, 'event': event, 'event_date': event.date,
        'is_upcoming': event.date >= date.today(),
    })


def event_detail_by_slug(request, slug: str):
    """Preferred PR10 URL; the integer endpoint is kept for PR9 compatibility."""
    event = get_object_or_404(Event.objects.select_related('user'), slug=slug)
    return render(request, 'events_web/event_detail.html', {
        'page_title': event.name, 'event': event, 'event_date': event.date,
        'is_upcoming': event.date >= date.today(),
    })


def search_by_date(request):
    selected_date = request.GET.get('date', '').strip()
    found = Event.objects.none()
    error = ''
    if selected_date:
        try:
            parsed = date.fromisoformat(selected_date)
            if parsed.isoformat() != selected_date:
                raise ValueError('Неверный формат')
            found = Event.objects.filter(date=parsed).select_related('user').order_by('name', 'pk')
        except ValueError:
            error = 'Укажите дату в формате ГГГГ-ММ-ДД.'
    return render(request, 'events_web/event_search.html', {
        'page_title': 'Поиск по дате', 'events': found, 'selected_date': selected_date,
        'has_searched': bool(selected_date and not error), 'error': error,
    })


def available_guests(request):
    selected_id = request.GET.get('event_id', '').strip()
    available = Guest.objects.none()
    error = ''
    if selected_id:
        if not selected_id.isdecimal() or int(selected_id) < 1:
            error = 'Выберите событие из списка.'
        elif not Event.objects.filter(pk=int(selected_id)).exists():
            error = 'Событие не найдено.'
        else:
            invited_ids = Invitation.objects.filter(
                event_id=int(selected_id), status=Invitation.STATUS_ACTIVE,
                guest_id__isnull=False,
            ).values('guest_id')
            available = Guest.objects.exclude(pk__in=invited_ids).order_by('name', 'pk')
    return render(request, 'events_web/available_guests.html', {
        'page_title': 'Свободные гости', 'events': Event.objects.all(),
        'available': available, 'selected_id': selected_id,
        'searched': bool(selected_id and not error), 'error': error,
    })
