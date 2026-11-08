"""Organizers, separate from django.contrib.auth.User."""
from django.db import models


class User(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField(max_length=254)

    class Meta:
        ordering = ['name', 'pk']
        verbose_name = 'Организатор'
        verbose_name_plural = 'Организаторы'

    def __str__(self):
        return f'{self.name} <{self.email}>'
