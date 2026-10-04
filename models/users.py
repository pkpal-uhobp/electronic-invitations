"""Класс пользователя предметной области ПР3/ПР5."""


class User:
    """Пользователь-организатор, который создаёт события."""

    def __init__(self, user_id: str, name: str, email: str) -> None:
        self.id = str(user_id)
        self.name = name
        self.email = email

    @classmethod
    def from_data(cls, data: dict) -> "User":
        """Создать пользователя из словаря JSON."""
        return cls(str(data["id"]), data["name"], data["email"])

    def __str__(self) -> str:
        return f"{self.name} <{self.email}>"
