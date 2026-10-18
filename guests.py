from models import Guest

def find_guest_by_id(guests: list[Guest], guest_id: int | str) -> Guest | None:
    return next((guest for guest in guests if guest.id == str(guest_id)), None)

def sort_guests(guests: list[Guest]) -> list[Guest]:
    return sorted(guests, key=lambda guest: (guest.name.lower(), int(guest.id)))
