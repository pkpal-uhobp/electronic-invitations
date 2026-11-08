# Generated for PR9 (equivalent to Django 5.2 makemigrations output).
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = [('users_web', '0001_initial')]
    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('date', models.DateField(db_index=True)),
                ('user', models.ForeignKey(blank=True, null=True,
                                           on_delete=django.db.models.deletion.SET_NULL,
                                           related_name='events', to='users_web.user')),
            ],
            options={
                'verbose_name': 'Событие',
                'verbose_name_plural': 'События',
                'ordering': ['date', 'name', 'pk'],
            },
        ),
    ]
