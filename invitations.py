"""Functions for creating and processing electronic invitations."""

from datetime import date


Invitations = list[dict[str, str]]
Invitation = dict[str, str]

VALID_RESPONSES = {"да", "нет", "не знаю"}


def create_invitation(
    event_name: str,
    guest_name: str,
    event_date: date,
) -> str:
    """Build the invitation text used in the original PR1 scenario."""
    return (
        f"Здравствуйте, {guest_name}!\n"
        f"Приглашаем вас на событие «{event_name}».\n"
        f"Дата проведения: {event_date}."
    )


def process_response(response: str) -> str:
    """Convert a guest response into a readable status."""
    normalized_response = response.strip().lower()
    if normalized_response == "да":
        return "Гость подтвердил участие."
    if normalized_response == "нет":
        return "Гость отказался от участия."
    return "Ответ гостя пока не определён."


def is_invitation_available(
    invitations: Invitations,
    event_id: str,
    guest_name: str,
) -> bool:
    """Check that the guest has no active invitation for the event."""
    normalized_name = guest_name.strip().lower()
    for invitation in invitations:
        same_event = invitation["event_id"] == event_id
        same_guest = invitation["guest_name"].lower() == normalized_name
        if same_event and same_guest and invitation["status"] != "cancelled":
            return False
    return True


def add_invitation(
    invitations: Invitations,
    event_id: str,
    guest_name: str,
) -> Invitation:
    """Create and append a new invitation record."""
    if not guest_name.strip():
        raise ValueError("Имя гостя не может быть пустым")
    if not is_invitation_available(invitations, event_id, guest_name):
        raise ValueError("Активное приглашение уже существует")

    invitation_id = str(
        max((int(item["id"]) for item in invitations), default=0) + 1
    )
    invitation = {
        "id": invitation_id,
        "event_id": event_id,
        "guest_name": guest_name.strip(),
        "response": "не знаю",
        "status": "active",
    }
    invitations.append(invitation)
    return invitation


def cancel_invitation(
    invitations: Invitations,
    invitation_id: str,
) -> bool:
    """Cancel an invitation by identifier."""
    for invitation in invitations:
        if invitation["id"] == invitation_id:
            invitation["status"] = "cancelled"
            return True
    return False


def set_response(
    invitations: Invitations,
    invitation_id: str,
    response: str,
) -> bool:
    """Save a guest response for an active invitation."""
    normalized_response = response.strip().lower()
    if normalized_response not in VALID_RESPONSES:
        raise ValueError("Допустимые ответы: да, нет, не знаю")

    for invitation in invitations:
        if invitation["id"] == invitation_id:
            if invitation["status"] == "cancelled":
                raise ValueError("Приглашение отменено")
            invitation["response"] = normalized_response
            return True
    return False


def find_invitations(
    invitations: Invitations,
    query: str,
) -> Invitations:
    """Find invitations by a substring of the guest name."""
    normalized_query = query.strip().lower()
    return [
        invitation
        for invitation in invitations
        if normalized_query in invitation["guest_name"].lower()
    ]


def sort_invitations(invitations: Invitations) -> Invitations:
    """Return invitations sorted by guest name and identifier."""
    return sorted(
        invitations,
        key=lambda item: (item["guest_name"].lower(), int(item["id"])),
    )


def invitation_statistics(invitations: Invitations) -> dict[str, int]:
    """Calculate invitation totals by response and status."""
    statistics = {
        "total": len(invitations),
        "active": 0,
        "cancelled": 0,
        "yes": 0,
        "no": 0,
        "unknown": 0,
    }

    for invitation in invitations:
        if invitation["status"] == "cancelled":
            statistics["cancelled"] += 1
            continue

        statistics["active"] += 1
        if invitation["response"] == "да":
            statistics["yes"] += 1
        elif invitation["response"] == "нет":
            statistics["no"] += 1
        else:
            statistics["unknown"] += 1

    return statistics
