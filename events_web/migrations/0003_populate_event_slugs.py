"""Backfill readable English slugs for all PR9 events without changing IDs."""
from django.db import migrations
from django.utils.text import slugify
from unidecode import unidecode


def populate_event_slugs(apps, schema_editor):
    Event = apps.get_model('events_web', 'Event')
    for item in Event.objects.using(schema_editor.connection.alias).order_by('pk'):
        suffix = f'-{item.pk}'
        stem = (slugify(unidecode(item.name)) or 'event')[:180 - len(suffix)].rstrip('-')
        item.slug = f'{stem or "event"}{suffix}'
        item.save(update_fields=['slug'])


class Migration(migrations.Migration):
    dependencies = [('events_web', '0002_event_slug')]
    operations = [migrations.RunPython(populate_event_slugs, migrations.RunPython.noop)]
