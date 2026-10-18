from models import User

def find_user_by_id(users: list[User], user_id: int | str) -> User | None:
    return next((user for user in users if user.id == str(user_id)), None)

def sort_users(users: list[User]) -> list[User]:
    return sorted(users, key=lambda user: (user.name.lower(), int(user.id)))
