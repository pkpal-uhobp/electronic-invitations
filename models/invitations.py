
class Invitation:
    def __init__(self, invitation_id: str, event, guest_name: str) -> None:
        self.id = invitation_id
        self.event = event
        self.guest_name = guest_name
        self.response = "не знаю"
        self.status = "active"

    def cancel(self) -> None:
        self.status = "cancelled"

    def set_response(self, response: str) -> None:
        self.response = response

    def __str__(self) -> str:
        return f"#{self.id}: {self.guest_name} - {self.status}"
