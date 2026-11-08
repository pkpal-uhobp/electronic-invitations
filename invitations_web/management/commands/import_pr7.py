"""PR7 SQLite -> PR9 Django ORM, preserving primary keys and foreign keys."""
import sqlite3
from datetime import date
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from events_web.models import Event
from guests_web.models import Guest
from invitations_web.models import Invitation
from users_web.models import User

TABLES = ('users', 'guests', 'events', 'invitations')


class Command(BaseCommand):
    help = 'Перенести данные ПР7 из отдельной SQLite в Django ORM (повторный запуск безопасен).'

    def add_arguments(self, parser):
        parser.add_argument('--source', type=Path,
                            default=settings.BASE_DIR / 'data' / 'invitations.sqlite',
                            help='Путь к предметной базе данных ПР7')

    def handle(self, *args, **options):
        source = options['source'].resolve()
        target = Path(settings.DATABASES['default']['NAME']).resolve()
        if source == target:
            raise CommandError('Исходная и целевая база не должны совпадать.')
        if not source.is_file():
            raise CommandError(f'База ПР7 не найдена: {source}')
        try:
            with sqlite3.connect(f'{source.as_uri()}?mode=ro', uri=True) as conn:
                conn.row_factory = sqlite3.Row
                present = {r['name'] for r in conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='table'")}
                if not set(TABLES).issubset(present):
                    raise CommandError('В источнике отсутствуют таблицы ПР7: '
                                       + ', '.join(sorted(set(TABLES) - present)))
                rows = {table: [dict(r) for r in conn.execute(
                    f'SELECT * FROM {table} ORDER BY id')] for table in TABLES}
        except sqlite3.Error as exc:
            raise CommandError(f'Ошибка чтения SQLite: {exc}') from exc

        # Every write is through ORM. Nothing in the old SQLite file is modified.
        try:
            with transaction.atomic():
                for row in rows['users']:
                    User.objects.update_or_create(
                        pk=row['id'], defaults={'name': row['name'], 'email': row['email']})
                for row in rows['guests']:
                    Guest.objects.update_or_create(
                        pk=row['id'], defaults={'name': row['name'], 'email': row['email']})
                for row in rows['events']:
                    Event.objects.update_or_create(
                        pk=row['id'], defaults={
                            'name': row['name'], 'date': date.fromisoformat(row['date']),
                            'user_id': row['user_id'],
                        })
                for row in rows['invitations']:
                    Invitation.objects.update_or_create(
                        pk=row['id'], defaults={
                            'event_id': row['event_id'], 'guest_id': row['guest_id'],
                            'guest_name': row['guest_name'],
                            'response': row['response'], 'status': row['status'],
                        })
        except Exception as exc:
            # Django IntegrityError and ValidationError must also abort transaction.
            raise CommandError(f'Перенос прерван, изменения отменены: {exc}') from exc
        counts = ', '.join(f'{name}: {len(rows[name])}' for name in TABLES)
        self.stdout.write(self.style.SUCCESS(f'Данные ПР7 перенесены: {counts}'))
