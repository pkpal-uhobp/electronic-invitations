"""ПР7: сводка из отдельной SQLite-базы, отображаемая шаблоном ПР6."""
from django.shortcuts import render
from db import queries


def index(request):
    totals = queries.one('total_counts')
    return render(request, 'homepage/index.html', {
        'page_title': 'Главная',
        'stats': {key: totals[key] for key in ('events', 'invitations', 'users', 'guests')},
    })
