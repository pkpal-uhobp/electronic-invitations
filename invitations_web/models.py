"""Electronic invitations with event, guest, response, and cancellation status."""
from django.db import models


class Invitation(models.Model):
    RESPONSE_YES = 'да'
    RESPONSE_NO = 'нет'
    RESPONSE_UNKNOWN = 'не знаю'
    STATUS_ACTIVE = 'active'
    STATUS_CANCELLED = 'cancelled'

    event = models.ForeignKey('events_web.Event', on_delete=models.CASCADE,
                              related_name='invitations')
    guest = models.ForeignKey('guests_web.Guest', null=True, blank=True,
                              on_delete=models.SET_NULL, related_name='invitations')
    guest_name = models.CharField(max_length=200)
    response = models.CharField(max_length=20, default=RESPONSE_UNKNOWN, choices=[
        (RESPONSE_YES, 'Да'), (RESPONSE_NO, 'Нет'),
        (RESPONSE_UNKNOWN, 'Не знаю'),
    ])
    status = models.CharField(max_length=20, default=STATUS_ACTIVE, db_index=True,
                              choices=[(STATUS_ACTIVE, 'Активно'),
                                       (STATUS_CANCELLED, 'Отменено')])

    class Meta:
        ordering = ['pk']
        verbose_name = 'Приглашение'
        verbose_name_plural = 'Приглашения'

    def cancel(self):
        self.status = self.STATUS_CANCELLED
        self.save(update_fields=['status'])

    def set_response(self, response):
        if response not in (self.RESPONSE_YES, self.RESPONSE_NO, self.RESPONSE_UNKNOWN):
            raise ValueError('Недопустимый ответ')
        self.response = response
        self.save(update_fields=['response'])

    def __str__(self):
        return f'#{self.pk}: {self.guest_name} — {self.status}'
