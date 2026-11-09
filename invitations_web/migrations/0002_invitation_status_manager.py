"""Extend existing PR9 string status; preserve old active/cancelled data."""
import django.db.models.deletion
from django.db import migrations, models
from django.db.models import Q


class Migration(migrations.Migration):
    dependencies = [('invitations_web', '0001_initial')]
    operations = [
        migrations.AlterField(
            model_name='invitation', name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                 related_name='invitations', to='events_web.event', verbose_name='Событие'),
        ),
        migrations.AlterField(
            model_name='invitation', name='guest',
            field=models.ForeignKey(blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL, related_name='invitations',
                to='guests_web.guest', verbose_name='Гость из справочника'),
        ),
        migrations.AlterField(
            model_name='invitation', name='guest_name',
            field=models.CharField(max_length=200, verbose_name='Имя приглашённого'),
        ),
        migrations.AlterField(
            model_name='invitation', name='response',
            field=models.CharField(max_length=20, default='не знаю',
                choices=[('да', 'Да'), ('нет', 'Нет'), ('не знаю', 'Не знаю')],
                verbose_name='Ответ гостя'),
        ),
        migrations.AlterField(
            model_name='invitation', name='status',
            field=models.CharField(max_length=20, default='active', db_index=True,
                choices=[('active', 'Активно'), ('cancelled', 'Отменено'),
                         ('completed', 'Завершено')], verbose_name='Статус'),
        ),
        migrations.AddConstraint(
            model_name='invitation',
            constraint=models.UniqueConstraint(
                fields=['event', 'guest'],
                condition=Q(status='active', guest__isnull=False),
                name='unique_active_invitation_event_guest'),
        ),
    ]
