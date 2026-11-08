# Generated for PR9 (equivalent to Django 5.2 makemigrations output).
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = [('events_web', '0001_initial'), ('guests_web', '0001_initial')]
    operations = [
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False, verbose_name='ID')),
                ('guest_name', models.CharField(max_length=200)),
                ('response', models.CharField(choices=[('да', 'Да'), ('нет', 'Нет'),
                                                      ('не знаю', 'Не знаю')],
                                              default='не знаю', max_length=20)),
                ('status', models.CharField(choices=[('active', 'Активно'),
                                                    ('cancelled', 'Отменено')],
                                            db_index=True, default='active', max_length=20)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                            related_name='invitations', to='events_web.event')),
                ('guest', models.ForeignKey(blank=True, null=True,
                                            on_delete=django.db.models.deletion.SET_NULL,
                                            related_name='invitations', to='guests_web.guest')),
            ],
            options={
                'verbose_name': 'Приглашение',
                'verbose_name_plural': 'Приглашения',
                'ordering': ['pk'],
            },
        ),
    ]
