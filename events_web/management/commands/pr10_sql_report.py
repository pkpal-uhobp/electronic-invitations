"""Show real SQL queries behind existing PR9/PR10 pages (development only)."""

from django.core.management.base import BaseCommand
from django.db import connection
from django.test import Client
from django.test.utils import CaptureQueriesContext
from django.urls import reverse

from invitations_web.models import Invitation


class Command(BaseCommand):
    help = 'Посчитать и показать SQL-запросы страниц; данные не изменяются.'

    def add_arguments(self, parser):
        parser.add_argument('--show-sql', action='store_true',
                            help='Показать SQL каждого запроса.')

    def handle(self, *args, **options):
        client = Client()
        pages = (
            ('Главная', reverse('homepage:index')),
            ('События', reverse('events:list')),
            ('Приглашения', reverse('invitations:list')),
            ('Статистика', reverse('invitations:statistics')),
        )
        for title, url in pages:
            with CaptureQueriesContext(connection) as captured:
                response = client.get(url)
            self.stdout.write(f'{title}: HTTP {response.status_code}, SQL: {len(captured)}')
            if options['show_sql']:
                for index, item in enumerate(captured, start=1):
                    self.stdout.write(f'  [{index}] {item["sql"]}')
        self.stdout.write('Пример QuerySet с select_related:')
        qs = Invitation.objects.select_related('event', 'guest', 'event__user')
        self.stdout.write(str(qs.query))
        self.stdout.write('Для анализа конкретных запросов в браузере используйте '
                          'панель SQL Django Debug Toolbar (DJANGO_DEBUG=1).')
