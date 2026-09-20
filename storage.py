"""JSON storage helpers for the project."""

import json
from pathlib import Path
from typing import Any

from events import Events
from invitations import Invitations


DATA_DIR = Path(__file__).parent / "data"
EVENTS_FILE = DATA_DIR / "events.json"
INVITATIONS_FILE = DATA_DIR / "invitations.json"


def load_json(path: Path, default: Any) -> Any:
    """Load JSON data and return a default value when reading fails."""
    try:
        with path.open("r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return default.copy()


def save_json(path: Path, data: Any) -> None:
    """Save data as formatted UTF-8 JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
    except OSError as error:
        raise RuntimeError("Не удалось сохранить данные") from error


def load_events() -> Events:
    """Load events from the project data file."""
    return load_json(EVENTS_FILE, {})


def save_events(events: Events) -> None:
    """Save events to the project data file."""
    save_json(EVENTS_FILE, events)


def load_invitations() -> Invitations:
    """Load invitations from the project data file."""
    return load_json(INVITATIONS_FILE, [])


def save_invitations(invitations: Invitations) -> None:
    """Save invitations to the project data file."""
    save_json(INVITATIONS_FILE, invitations)
