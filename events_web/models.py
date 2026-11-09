"""Events with readable URLs and a database-generated title length (PR10)."""
from django.db import models, transaction
from django.db.models.functions import Length
from django.urls import reverse
from django.utils.text import slugify
from unidecode import unidecode


def event_slug(name, pk):
    """Deterministic transliterated slug; ID avoids same-name collisions."""
    suffix = f'-{pk}'
    stem = slugify(unidecode(name)) or 'event'
    stem = stem[:180 - len(suffix)].rstrip('-') or 'event'
    return f'{stem}{suffix}'


class Event(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название события')
    date = models.DateField(db_index=True, verbose_name='Дата проведения')
    user = models.ForeignKey(
        'users_web.User', null=True, blank=True, on_delete=models.SET_NULL,
        related_name='events', verbose_name='Организатор',
    )
    slug = models.SlugField(
        max_length=180, unique=True, null=True, blank=True, editable=False,
        verbose_name='URL-идентификатор',
    )
    name_length = models.GeneratedField(
        expression=Length('name'), output_field=models.PositiveIntegerField(),
        db_persist=False, verbose_name='Длина названия',
    )

    class Meta:
        ordering = ['date', 'name', 'pk']
        verbose_name = 'Событие'
        verbose_name_plural = 'События'

    def save(self, *args, **kwargs):
        """Generate slug when saved; keep existing slugs stable after renames."""
        if self.slug:
            return super().save(*args, **kwargs)
        if self.pk is not None:
            self.slug = event_slug(self.name, self.pk)
            if kwargs.get('update_fields') is not None:
                kwargs['update_fields'] = set(kwargs['update_fields']) | {'slug'}
            return super().save(*args, **kwargs)
        with transaction.atomic():
            # Unique nullable slug permits an initial INSERT before obtaining PK.
            super().save(*args, **kwargs)
            self.slug = event_slug(self.name, self.pk)
            type(self).objects.filter(pk=self.pk).update(slug=self.slug)

    def get_absolute_url(self):
        return reverse('events:detail_slug', kwargs={'slug': self.slug})

    def __str__(self):
        return f'{self.name} — {self.date:%Y-%m-%d}'
