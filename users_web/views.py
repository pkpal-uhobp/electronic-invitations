"""ПР7: организаторы и их мероприятия из SQL."""
from django.http import Http404
from django.shortcuts import render
from db import queries, repository


def users(request):
    return render(request, 'users_web/user_list.html', {
        'page_title': 'Организаторы', 'users': repository.users(),
    })


def user_detail(request, user_id: int):
    row = queries.one('user_by_id', (user_id,))
    if row is None:
        raise Http404('Организатор не найден')
    return render(request, 'users_web/user_detail.html', {
        'page_title': row['name'], 'user': repository.user_from_row(row),
        'events': repository.events('events_for_user', (user_id,)),
    })
