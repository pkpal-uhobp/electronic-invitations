"""SQLite virtual generated column (works when existing event records exist)."""
from django.db import migrations, models
from django.db.models.functions import Length


class Migration(migrations.Migration):
    dependencies = [('events_web', '0003_populate_event_slugs')]
    operations = [migrations.AddField(
        model_name='event', name='name_length',
        field=models.GeneratedField(
            db_persist=False, expression=Length('name'),
            output_field=models.PositiveIntegerField(), verbose_name='Длина названия'),
    )]
