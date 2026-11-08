"""Events and optional organizers."""
from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField(db_index=True)
    user = models.ForeignKey(
        'users_web.User', null=True, blank=True, on_delete=models.SET_NULL,
        related_name='events',
    )

    class Meta:
        ordering = ['date', 'name', 'pk']
        verbose_name = 'Событие'
        verbose_name_plural = 'События'

    def __str__(self):
        return f'{self.name} — {self.date:%Y-%m-%d}'
