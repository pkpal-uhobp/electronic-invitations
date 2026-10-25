"""ПР7: приглашения, фильтрация и статистика из SQL."""
from datetime import date
from django.http import Http404
from django.shortcuts import render
from db import queries, repository


def invitations(request):
    status = request.GET.get('status', '').strip()
    if status not in ('active', 'cancelled'):
        status = ''
    if status:
        result = repository.invitations('invitations_by_status', (status,))
    else:
        result = repository.invitations()
    return render(request, 'invitations_web/invitation_list.html', {
        'page_title': 'Приглашения', 'invitations': result, 'selected_status': status,
    })


def invitation_detail(request, invitation_id: int):
    row = queries.one('invitation_by_id', (invitation_id,))
    if row is None:
        raise Http404('Приглашение не найдено')
    invitation = repository.invitation_from_row(row)
    return render(request, 'invitations_web/invitation_detail.html', {
        'page_title': f'Приглашение №{invitation.id}', 'invitation': invitation,
        'event_date': date.fromisoformat(invitation.event.date),
    })


def statistics(request):
    return render(request, 'invitations_web/statistics.html', {
        'page_title': 'Статистика приглашений',
        'totals': queries.one('invitation_totals'),
        'by_event': queries.rows('invitations_by_event'),
        'by_response': queries.rows('invitations_by_response'),
        'by_organizer': queries.rows('organizer_event_counts'),
        'popular': queries.rows('popular_events', (2,)),
    })
