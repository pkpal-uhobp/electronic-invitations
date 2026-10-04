"""Функции работы с пользователями предметной области."""

from models import User


def find_user_by_id(users: list[User], user_id: int | str) -> User | None:
    """Найти пользователя по идентификатору."""
    target = str(user_id)
    for user in users:
        if user.id == target:
            return user
    return None


def sort_users(users: list[User]) -> list[User]:
    """Отсортировать пользователей по имени и идентификатору."""
    return sorted(users, key=lambda user: (user.name.lower(), int(user.id)))
