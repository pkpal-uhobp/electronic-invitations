"""Класс гостя предметной области ПР3/ПР5."""


class Guest:
    """Гость, которому могут быть отправлены приглашения на события."""

    def __init__(self, guest_id: str, name: str, email: str) -> None:
        self.id = str(guest_id)
        self.name = name
        self.email = email

    @classmethod
    def from_data(cls, data: dict) -> "Guest":
        """Создать гостя из словаря JSON."""
        return cls(str(data["id"]), data["name"], data["email"])

    def __str__(self) -> str:
        return f"{self.name} <{self.email}>"
