
from datetime import date

class Event:
    def __init__(self, event_id: str, name: str, event_date: str) -> None:
        self.id = event_id
        self.name = name
        self.date = event_date

    def __str__(self) -> str:
        return f"{self.name} - {self.date}"

    def is_valid(self) -> bool:
        return bool(self.name.strip()) and date.fromisoformat(self.date) >= date.today()
