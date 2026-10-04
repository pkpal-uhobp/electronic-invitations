from models import Guest
from guests import find_guest_by_id, sort_guests


def test_find_and_sort_guests() -> None:
    guests = [
        Guest("2", "Иван", "ivan@example.com"),
        Guest("1", "Анна", "anna@example.com"),
    ]

    assert find_guest_by_id(guests, "2").name == "Иван"
    assert [guest.id for guest in sort_guests(guests)] == ["1", "2"]
