"""Гость (предметная модель)."""
class Guest:
    def __init__(self, guest_id: str, name: str, email: str):
        self.id = str(guest_id)
        self.name = name
        self.email = email

    @classmethod
    def from_data(cls, data: dict):
        return cls(str(data["id"]), data["name"], data["email"])

    def __str__(self):
        return f"{self.name} <{self.email}>"
