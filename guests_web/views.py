"""ПР7: гости и связанные приглашения из SQL."""
from django.http import Http404
from django.shortcuts import render
from db import queries, repository


def guests(request):
    return render(request, 'guests_web/guest_list.html', {
        'page_title': 'Гости', 'guests': repository.guests(),
    })


def guest_detail(request, guest_id: int):
    row = queries.one('guest_by_id', (guest_id,))
    if row is None:
        raise Http404('Гость не найден')
    return render(request, 'guests_web/guest_detail.html', {
        'page_title': row['name'], 'guest': repository.guest_from_row(row),
        'invitations': repository.invitations('invitations_for_guest', (guest_id,)),
    })
