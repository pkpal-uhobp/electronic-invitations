"""Homepage counts from Django ORM, not sqlite3."""
from django.shortcuts import render

from events_web.models import Event
from guests_web.models import Guest
from invitations_web.models import Invitation
from users_web.models import User


def index(request):
    stats = {'events': Event.objects.count(), 'invitations': Invitation.objects.count(),
             'users': User.objects.count(), 'guests': Guest.objects.count()}
    return render(request, 'homepage/index.html', {'page_title': 'Главная', 'stats': stats})
