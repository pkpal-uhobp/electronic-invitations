"""Пользователи-организаторы, без Django Auth и ORM."""
from django.http import Http404
from django.shortcuts import render
from storage import load_events, load_users
from users import find_user_by_id, sort_users


def users(request):
    user_list = sort_users(load_users())
    event_list = load_events(user_list)
    counts = {u.id: sum(e.user is not None and e.user.id == u.id for e in event_list)
              for u in user_list}
    return render(request, 'users_web/user_list.html', {
        'page_title': 'Организаторы', 'users': user_list, 'counts': counts,
    })


def user_detail(request, user_id: int):
    user_list = load_users()
    user = find_user_by_id(user_list, user_id)
    if user is None:
        raise Http404('Организатор не найден')
    event_list = [e for e in load_events(user_list) if e.user and e.user.id == user.id]
    return render(request, 'users_web/user_detail.html', {
        'page_title': user.name, 'user': user, 'events': event_list,
    })
