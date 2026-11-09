"""Shared project values for the site shell; no duplicate view boilerplate."""
from .models import Event


def invitations_context(request):
    return {
        'site_name': 'Электронные приглашения',
        'events_count': Event.objects.count(),
    }
