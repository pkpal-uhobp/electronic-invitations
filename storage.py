"""Совместимое с ПР5 JSON-хранилище; Django ORM не используется."""
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
    file_path = Path(path)
    if not file_path.exists():
        return default
    try:
        with file_path.open("r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return default

def save_json(path: str | Path, data: Any) -> None:
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with file_path.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

def load_users():
    return [User.from_data(item) for item in load_json(USERS_FILE, [])]

def save_users(users):
    save_json(USERS_FILE, [{"id": u.id, "name": u.name, "email": u.email} for u in users])

def load_guests():
    return [Guest.from_data(item) for item in load_json(GUESTS_FILE, [])]

def save_guests(guests):
    save_json(GUESTS_FILE, [{"id": g.id, "name": g.name, "email": g.email} for g in guests])

def load_events(users=None):
    if users is None:
        users = load_users()
    result = []
    for item in load_json(EVENTS_FILE, []):
        user = next((u for u in users if u.id == str(item.get("user_id", ""))), None)
        result.append(Event(str(item["id"]), item["name"], item["date"], user))
    return result

def save_events(events):
    data = []
    for e in events:
        item = {"id": e.id, "name": e.name, "date": e.date}
        if e.user is not None:
            item["user_id"] = e.user.id
        data.append(item)
    save_json(EVENTS_FILE, data)

def load_invitations(events, guests=None):
    if guests is None:
        guests = load_guests()
    result = []
    for item in load_json(INVITATIONS_FILE, []):
        event = next((e for e in events if e.id == str(item["event_id"])), None)
        if event is None:
            continue
        guest = next((g for g in guests if g.id == str(item.get("guest_id", ""))), None)
        if guest is None:
            guest = item.get("guest_name", "Неизвестный гость")
        invitation = Invitation(str(item["id"]), event, guest)
        invitation.response = item.get("response", "не знаю")
        invitation.status = item.get("status", "active")
        result.append(invitation)
    return result

def save_invitations(invitations):
    data = []
    for i in invitations:
        item = {"id": i.id, "event_id": i.event.id, "guest_name": i.guest_name,
                "response": i.response, "status": i.status}
        if isinstance(i.guest, Guest):
            item["guest_id"] = i.guest.id
        data.append(item)
    save_json(INVITATIONS_FILE, data)
