from models import User
from users import find_user_by_id, sort_users


def test_find_and_sort_users() -> None:
    users = [
        User("2", "Яна", "yana@example.com"),
        User("1", "Анна", "anna@example.com"),
    ]

    assert find_user_by_id(users, 1).email == "anna@example.com"
    assert [user.id for user in sort_users(users)] == ["1", "2"]
