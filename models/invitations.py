"""Класс электронного приглашения предметной области ПР3."""

from .guests import Guest


class Invitation:
    """Приглашение конкретного гостя на конкретное событие."""

    def __init__(self, invitation_id: str, event, guest) -> None:
        self.id = str(invitation_id)
        self.event = event
        self.guest = guest
        self.response = "не знаю"
        self.status = "active"

    @property
    def guest_name(self) -> str:
        """Имя гостя; свойство сохраняет совместимость со старым кодом ПР3."""
        if isinstance(self.guest, Guest):
            return self.guest.name
        return str(self.guest)

    def cancel(self) -> None:
        """Отменить приглашение."""
        self.status = "cancelled"

    def set_response(self, response: str) -> None:
        """Сохранить ответ гостя."""
        self.response = response

    def __str__(self) -> str:
        return f"#{self.id}: {self.guest_name} - {self.status}"
