"""Invitees/guests."""
from django.db import models


class Guest(models.Model):
    name = models.CharField(max_length=120, verbose_name='Имя')
    email = models.EmailField(max_length=254, verbose_name='Электронная почта')

    class Meta:
        ordering = ['name', 'pk']
        verbose_name = 'Гость'
        verbose_name_plural = 'Гости'

    def __str__(self):
        return f'{self.name} <{self.email}>'
