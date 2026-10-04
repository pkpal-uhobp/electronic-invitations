"""Работа с электронными приглашениями."""

from models import Event, Guest, Invitation

VALID_RESPONSES = {"да", "нет", "не знаю"}


def _next_id(invitations) -> str:
    """Вернуть следующий идентификатор приглашения."""
    ids = []
    for invitation in invitations:
        if isinstance(invitation, dict):
            ids.append(str(invitation["id"]))
        else:
            ids.append(str(invitation.id))
    return str(max((int(value) for value in ids), default=0) + 1)


def _guest_name(guest) -> str:
    """Вернуть имя гостя для строки, Guest или объекта Invitation."""
    if isinstance(guest, Guest):
        return guest.name
    return str(guest)


def is_invitation_available(invitations, event_id, guest) -> bool:
    """Проверить, можно ли создать активное приглашение этому гостю."""
    target_event_id = str(getattr(event_id, "id", event_id))
    target_guest = _guest_name(guest).strip().lower()

    for invitation in invitations:
        if isinstance(invitation, dict):
            current_event_id = str(invitation["event_id"])
            current_guest = invitation["guest_name"].strip().lower()
            status = invitation.get("status", "active")
        else:
            current_event_id = str(invitation.event.id)
            current_guest = invitation.guest_name.strip().lower()
            status = invitation.status

        if (
            current_event_id == target_event_id
            and current_guest == target_guest
            and status == "active"
        ):
            return False
    return True


def add_invitation(invitations, event, guest):
    """Создать приглашение в формате ПР2 или объектном формате ПР3/ПР5."""
    guest_name = _guest_name(guest).strip()
    if not guest_name:
        raise ValueError("Имя гостя не может быть пустым")
    if not is_invitation_available(invitations, event, guest):
        raise ValueError("Активное приглашение для гостя уже существует")

    invitation_id = _next_id(invitations)
    if isinstance(event, Event):
        invitation = Invitation(invitation_id, event, guest)
    else:
        invitation = {
            "id": invitation_id,
            "event_id": str(event),
            "guest_name": guest_name,
            "response": "не знаю",
            "status": "active",
        }

    invitations.append(invitation)
    return invitation


def cancel_invitation(invitations, invitation_id: str) -> bool:
    """Отменить приглашение по идентификатору."""
    target = str(invitation_id)
    for invitation in invitations:
        current_id = str(
            invitation["id"] if isinstance(invitation, dict) else invitation.id
        )
        if current_id != target:
            continue
        if isinstance(invitation, dict):
            invitation["status"] = "cancelled"
        else:
            invitation.cancel()
        return True
    return False


def set_response(invitations, invitation_id: str, response: str) -> bool:
    """Сохранить ответ гостя на приглашение."""
    if response not in VALID_RESPONSES:
        raise ValueError("Допустимые ответы: да, нет, не знаю")

    target = str(invitation_id)
    for invitation in invitations:
        current_id = str(
            invitation["id"] if isinstance(invitation, dict) else invitation.id
        )
        if current_id != target:
            continue
        if isinstance(invitation, dict):
            invitation["response"] = response
        else:
            invitation.set_response(response)
        return True
    return False


def sort_invitations(invitations):
    """Отсортировать приглашения по имени гостя и идентификатору."""

    def key(invitation):
        if isinstance(invitation, dict):
            return (
                invitation["guest_name"].lower(),
                int(invitation["id"]),
            )
        return invitation.guest_name.lower(), int(invitation.id)

    return sorted(invitations, key=key)


def find_invitations(invitations, query: str):
    """Найти приглашения по имени гостя."""
    query = query.lower()
    result = []
    for invitation in invitations:
        guest_name = (
            invitation["guest_name"]
            if isinstance(invitation, dict)
            else invitation.guest_name
        )
        if query in guest_name.lower():
            result.append(invitation)
    return result


def find_invitation_by_id(
    invitations: list[Invitation], invitation_id: int | str
) -> Invitation | None:
    """Найти объект Invitation по идентификатору для динамического URL."""
    target = str(invitation_id)
    for invitation in invitations:
        if invitation.id == target:
            return invitation
    return None


def create_invitation(event_name, guest_name, event_date):
    """Сформировать текст приглашения."""
    return (
        f"Здравствуйте, {guest_name}!\n"
        f"Приглашаем вас на событие «{event_name}».\n"
        f"Дата проведения: {event_date}."
    )


def process_response(response):
    """Вернуть человекочитаемое описание ответа гостя."""
    return {
        "да": "Гость подтвердил участие.",
        "нет": "Гость отказался от участия.",
    }.get(response, "Ответ гостя пока не определён.")


def invitation_statistics(invitations):
    """Посчитать основные показатели по приглашениям."""
    statistics = {
        "total": len(invitations),
        "active": 0,
        "cancelled": 0,
        "yes": 0,
        "no": 0,
        "unknown": 0,
    }

    for invitation in invitations:
        if isinstance(invitation, dict):
            status = invitation.get("status", "active")
            response = invitation.get("response", "не знаю")
        else:
            status = invitation.status
            response = invitation.response

        if status == "active":
            statistics["active"] += 1
        else:
            statistics["cancelled"] += 1

        if response == "да":
            statistics["yes"] += 1
        elif response == "нет":
            statistics["no"] += 1
        else:
            statistics["unknown"] += 1

    return statistics
