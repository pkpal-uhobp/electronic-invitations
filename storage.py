"""Хранилище объектов проекта в JSON."""
import json
from pathlib import Path
from typing import List

from models import Event, Invitation

DATA_DIR = Path(__file__).parent / "data"
EVENTS_FILE = DATA_DIR / "events.json"
INVITATIONS_FILE = DATA_DIR / "invitations.json"


def load_events() -> List[Event]:
    with EVENTS_FILE.open("r", encoding="utf-8") as file:
        data = json.load(file)
    return [Event(str(item["id"]), item["name"], item["date"]) for item in data]


def save_events(events: List[Event]) -> None:
    DATA_DIR.mkdir(exist_ok=True)
    with EVENTS_FILE.open("w", encoding="utf-8") as file:
        json.dump(
            [{"id": e.id, "name": e.name, "date": e.date} for e in events],
            file,
            ensure_ascii=False,
            indent=2,
        )


def load_invitations(events: List[Event]) -> List[Invitation]:
    with INVITATIONS_FILE.open("r", encoding="utf-8") as file:
        data = json.load(file)

    result = []
    for item in data:
        event = next((e for e in events if e.id == item["event_id"]), None)
        if event:
            invitation = Invitation(
                str(item["id"]), event, item["guest_name"]
            )
            invitation.response = item.get("response", "не знаю")
            invitation.status = item.get("status", "active")
            result.append(invitation)
    return result


def save_invitations(invitations: List[Invitation]) -> None:
    DATA_DIR.mkdir(exist_ok=True)
    with INVITATIONS_FILE.open("w", encoding="utf-8") as file:
        json.dump(
            [
                {
                    "id": i.id,
                    "event_id": i.event.id,
                    "guest_name": i.guest_name,
                    "response": i.response,
                    "status": i.status,
                }
                for i in invitations
            ],
            file,
            ensure_ascii=False,
            indent=2,
        )
