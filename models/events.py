"""Предметная модель события (ПР3–ПР6, не Django ORM)."""
from datetime import date

class Event:
    def __init__(self, event_id: str, name: str, event_date: str, user=None):
        self.id = str(event_id)
        self.name = name
        self.date = event_date
        self.user = user

    def __str__(self):
        return f"{self.name} - {self.date}"

    def is_valid(self):
        return bool(self.name.strip()) and date.fromisoformat(self.date) >= date.today()
