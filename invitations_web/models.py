"""Electronic invitations with status-aware ORM manager and admin validation."""
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q


class InvitationQuerySet(models.QuerySet):
    def active(self):
        return self.filter(status=self.model.Status.ACTIVE)

    def cancelled(self):
        return self.filter(status=self.model.Status.CANCELLED)

    def completed(self):
        return self.filter(status=self.model.Status.COMPLETED)

    def for_event(self, event):
        return self.filter(event=event)


class InvitationManager(models.Manager.from_queryset(InvitationQuerySet)):
    pass


class Invitation(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Активно'
        CANCELLED = 'cancelled', 'Отменено'
        COMPLETED = 'completed', 'Завершено'

    class Response(models.TextChoices):
        YES = 'да', 'Да'
        NO = 'нет', 'Нет'
        UNKNOWN = 'не знаю', 'Не знаю'

    # Backwards compatible names for PR9 tests and previous public API.
    STATUS_ACTIVE = Status.ACTIVE
    STATUS_CANCELLED = Status.CANCELLED
    STATUS_COMPLETED = Status.COMPLETED
    RESPONSE_YES = Response.YES
    RESPONSE_NO = Response.NO
    RESPONSE_UNKNOWN = Response.UNKNOWN

    event = models.ForeignKey(
        'events_web.Event', on_delete=models.CASCADE, related_name='invitations',
        verbose_name='Событие',
    )
    guest = models.ForeignKey(
        'guests_web.Guest', null=True, blank=True, on_delete=models.SET_NULL,
        related_name='invitations', verbose_name='Гость из справочника',
    )
    guest_name = models.CharField(max_length=200, verbose_name='Имя приглашённого')
    response = models.CharField(
        max_length=20, default=Response.UNKNOWN, choices=Response.choices,
        verbose_name='Ответ гостя',
    )
    status = models.CharField(
        max_length=20, default=Status.ACTIVE, db_index=True,
        choices=Status.choices, verbose_name='Статус',
    )
    objects = InvitationManager()

    class Meta:
        ordering = ['pk']
        verbose_name = 'Приглашение'
        verbose_name_plural = 'Приглашения'
        constraints = [
            models.UniqueConstraint(
                fields=['event', 'guest'],
                condition=Q(status='active', guest__isnull=False),
                name='unique_active_invitation_event_guest',
            ),
        ]

    def clean(self):
        """Prevent duplicate active invites in admin (including free-text guests)."""
        super().clean()
        if self.status != self.Status.ACTIVE or not self.event_id:
            return
        qs = type(self).objects.active().filter(event_id=self.event_id)
        if self.pk:
            qs = qs.exclude(pk=self.pk)
        if self.guest_id is not None:
            # For registered guests the ForeignKey identifies the person.
            is_duplicate = qs.filter(guest_id=self.guest_id).exists()
        else:
            # SQLite's case-insensitive LIKE/iexact handles ASCII only by default.
            # Compare free-text guest names in Python so Cyrillic case is respected.
            normalized_name = (self.guest_name or '').strip().casefold()
            is_duplicate = any(
                stored_name.strip().casefold() == normalized_name
                for stored_name in qs.filter(guest__isnull=True)
                .values_list('guest_name', flat=True)
            )
        if is_duplicate:
            raise ValidationError('Активное приглашение для этого гостя уже существует.')

    def cancel(self):
        self.status = self.Status.CANCELLED
        self.save(update_fields=['status'])

    def complete(self):
        self.status = self.Status.COMPLETED
        self.save(update_fields=['status'])

    def set_response(self, response):
        if response not in self.Response.values:
            raise ValueError('Недопустимый ответ')
        self.response = response
        self.save(update_fields=['response'])

    def __str__(self):
        return f'#{self.pk}: {self.guest_name} — {self.get_status_display()}'
