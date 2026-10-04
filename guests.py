"""Функции работы с гостями предметной области."""

from models import Guest


def find_guest_by_id(guests: list[Guest], guest_id: int | str) -> Guest | None:
    """Найти гостя по идентификатору."""
    target = str(guest_id)
    for guest in guests:
        if guest.id == target:
            return guest
    return None


def sort_guests(guests: list[Guest]) -> list[Guest]:
    """Отсортировать гостей по имени и идентификатору."""
    return sorted(guests, key=lambda guest: (guest.name.lower(), int(guest.id)))
