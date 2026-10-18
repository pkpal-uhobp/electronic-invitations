"""Приглашение (предметная модель)."""
from .guests import Guest

class Invitation:
    def __init__(self, invitation_id: str, event, guest):
        self.id = str(invitation_id)
        self.event = event
        self.guest = guest
        self.response = "не знаю"
        self.status = "active"

    @property
    def guest_name(self):
        return self.guest.name if isinstance(self.guest, Guest) else str(self.guest)

    def cancel(self):
        self.status = "cancelled"

    def set_response(self, response):
        self.response = response

    def __str__(self):
        return f"#{self.id}: {self.guest_name} - {self.status}"
