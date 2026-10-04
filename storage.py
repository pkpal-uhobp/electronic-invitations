"""Хранилище объектов проекта в JSON."""

import json
from pathlib import Path
from typing import Any

from models import Event, Guest, Invitation, User

DATA_DIR = Path(__file__).parent / "data"
EVENTS_FILE = DATA_DIR / "events.json"
INVITATIONS_FILE = DATA_DIR / "invitations.json"
USERS_FILE = DATA_DIR / "users.json"
GUESTS_FILE = DATA_DIR / "guests.json"


def load_json(path: str | Path, default: Any):
    """Загрузить произвольные JSON-данные или вернуть значение по умолчанию."""
    file_path = Path(path)
    if not file_path.exists():
        return default
    try:
        with file_path.open("r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return default


def save_json(path: str | Path, data: Any) -> None:
    """Сохранить произвольные данные в JSON."""
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with file_path.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def load_users() -> list[User]:
    """Загрузить пользователей из JSON."""
    return [User.from_data(item) for item in load_json(USERS_FILE, [])]


def save_users(users: list[User]) -> None:
    """Сохранить пользователей в JSON."""
    save_json(
        USERS_FILE,
        [
            {"id": user.id, "name": user.name, "email": user.email}
            for user in users
        ],
    )


def load_guests() -> list[Guest]:
    """Загрузить гостей из JSON."""
    return [Guest.from_data(item) for item in load_json(GUESTS_FILE, [])]


def save_guests(guests: list[Guest]) -> None:
    """Сохранить гостей в JSON."""
    save_json(
        GUESTS_FILE,
        [
            {"id": guest.id, "name": guest.name, "email": guest.email}
            for guest in guests
        ],
    )


def load_events(users: list[User] | None = None) -> list[Event]:
    """Загрузить события и восстановить связь с пользователем-организатором."""
    if users is None:
        users = load_users()

    result = []
    for item in load_json(EVENTS_FILE, []):
        user = next(
            (
                current
                for current in users
                if current.id == str(item.get("user_id", ""))
            ),
            None,
        )
        result.append(
            Event(
                str(item["id"]),
                item["name"],
                item["date"],
                user,
            )
        )
    return result


def save_events(events: list[Event]) -> None:
    """Сохранить объекты Event в JSON."""
    data = []
    for event in events:
        item = {"id": event.id, "name": event.name, "date": event.date}
        if event.user is not None:
            item["user_id"] = event.user.id
        data.append(item)
    save_json(EVENTS_FILE, data)


def load_invitations(
    events: list[Event],
    guests: list[Guest] | None = None,
) -> list[Invitation]:
    """Загрузить приглашения и восстановить связи с Event и Guest."""
    if guests is None:
        guests = load_guests()

    data = load_json(INVITATIONS_FILE, [])
    result = []
    for item in data:
        event = next(
            (
                current
                for current in events
                if current.id == str(item["event_id"])
            ),
            None,
        )
        if event is None:
            continue

        guest = next(
            (
                current
                for current in guests
                if current.id == str(item.get("guest_id", ""))
            ),
            None,
        )
        if guest is None:
            # Совместимость со старым форматом ПР3, где был только guest_name.
            guest = item.get("guest_name", "Неизвестный гость")

        invitation = Invitation(str(item["id"]), event, guest)
        invitation.response = item.get("response", "не знаю")
        invitation.status = item.get("status", "active")
        result.append(invitation)
    return result


def save_invitations(invitations: list[Invitation]) -> None:
    """Сохранить объекты Invitation в JSON."""
    data = []
    for invitation in invitations:
        item = {
            "id": invitation.id,
            "event_id": invitation.event.id,
            "guest_name": invitation.guest_name,
            "response": invitation.response,
            "status": invitation.status,
        }
        if isinstance(invitation.guest, Guest):
            item["guest_id"] = invitation.guest.id
        data.append(item)
    save_json(INVITATIONS_FILE, data)
