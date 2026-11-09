"""Seed from legacy PR7 only on an empty Django ORM database."""
from django.core.management import call_command
from django.core.management.base import BaseCommand
from events_web.models import Event
from guests_web.models import Guest
from invitations_web.models import Invitation
from users_web.models import User


class Command(BaseCommand):
    help = 'Импортировать PR7 только если все четыре целевые таблицы пусты.'

    def handle(self, *args, **options):
        counts = (Event.objects.count(), Guest.objects.count(),
                  Invitation.objects.count(), User.objects.count())
        if any(counts):
            self.stdout.write('База уже содержит данные; импорт PR7 пропущен.')
            return
        call_command('import_pr7')
