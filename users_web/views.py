"""Organizers and their related events via Django ORM."""
from django.shortcuts import get_object_or_404, render

from .models import User
from events_web.models import Event


def users(request):
    result = User.objects.all().order_by('name', 'pk')
    return render(request, 'users_web/user_list.html', {
        'page_title': 'Организаторы', 'users': result,
    })


def user_detail(request, user_id: int):
    user = get_object_or_404(User, pk=user_id)
    events = Event.objects.filter(user=user).select_related('user').order_by('date', 'pk')
    return render(request, 'users_web/user_detail.html', {
        'page_title': user.name, 'user': user, 'events': events,
    })
