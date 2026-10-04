"""Класс события предметной области ПР3."""

from datetime import date


class Event:
    """Событие, созданное пользователем и доступное для приглашений."""

    def __init__(
        self,
        event_id: str,
        name: str,
        event_date: str,
        user=None,
    ) -> None:
        self.id = str(event_id)
        self.name = name
        self.date = event_date
        self.user = user

    def __str__(self) -> str:
        return f"{self.name} - {self.date}"

    def is_valid(self) -> bool:
        """Проверить, что название заполнено, а дата не находится в прошлом."""
        return (
            bool(self.name.strip())
            and date.fromisoformat(self.date) >= date.today()
        )
