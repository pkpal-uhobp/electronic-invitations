"""В ПР6 HTML целиком формируется Django-шаблонами."""
from django.shortcuts import render
from storage import load_events, load_guests, load_invitations, load_users


def index(request):
    users = load_users()
    guests = load_guests()
    events = load_events(users)
    invitations = load_invitations(events, guests)
    return render(request, 'homepage/index.html', {
        'page_title': 'Главная',
        'stats': {
            'events': len(events), 'invitations': len(invitations),
            'guests': len(guests), 'users': len(users),
        },
    })
