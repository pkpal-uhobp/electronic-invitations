"""Console interface for the electronic invitations project."""

from datetime import date

from events import (
    add_event,
    find_events,
    iter_upcoming_events,
    sort_events,
)
from invitations import (
    add_invitation,
    cancel_invitation,
    create_invitation,
    find_invitations,
    invitation_statistics,
    process_response,
    set_response,
    sort_invitations,
)
from storage import (
    load_events,
    load_invitations,
    save_events,
    save_invitations,
)
from utils import input_date, input_int


MENU = """
1. Показать события
2. Добавить событие
3. Найти событие
4. Показать приглашения
5. Создать приглашение
6. Отменить приглашение
7. Сохранить ответ гостя
8. Найти приглашение
9. Показать статистику
0. Выход
"""


def show_events(events: dict[str, dict[str, str]]) -> None:
    """Print events sorted by date."""
    if not events:
        print("Событий пока нет.")
        return

    for event_id, event in sort_events(events):
        print(f"{event_id}. {event['name']} - {event['date']}")


def show_upcoming(events: dict[str, dict[str, str]]) -> None:
    """Print upcoming events using a generator."""
    upcoming = list(iter_upcoming_events(events))
    if not upcoming:
        print("Предстоящих событий нет.")
        return

    for event_id, event in upcoming:
        print(f"{event_id}. {event['name']} - {event['date']}")


def show_invitations(invitations: list[dict[str, str]]) -> None:
    """Print invitations sorted by guest name."""
    if not invitations:
        print("Приглашений пока нет.")
        return

    for invitation in sort_invitations(invitations):
        print(
            f"#{invitation['id']} | событие {invitation['event_id']} | "
            f"{invitation['guest_name']} | {invitation['response']} | "
            f"{invitation['status']}"
        )


def print_statistics(invitations: list[dict[str, str]]) -> None:
    """Print invitation statistics."""
    statistics = invitation_statistics(invitations)
    print(f"Всего приглашений: {statistics['total']}")
    print(f"Активных: {statistics['active']}")
    print(f"Отменённых: {statistics['cancelled']}")
    print(f"Подтвердили: {statistics['yes']}")
    print(f"Отказались: {statistics['no']}")
    print(f"Без ответа: {statistics['unknown']}")


def add_event_from_input(events: dict[str, dict[str, str]]) -> None:
    """Read event data from the user and append it to the collection."""
    name = input("Название события: ").strip()
    event_date = input_date("Дата события (ГГГГ-ММ-ДД): ")
    event_id = add_event(events, name, event_date)
    print(f"Событие добавлено. ID: {event_id}")


def create_invitation_from_input(
    events: dict[str, dict[str, str]],
    invitations: list[dict[str, str]],
) -> None:
    """Create an invitation record and print the invitation text."""
    if not events:
        print("Сначала добавьте событие.")
        return

    show_upcoming(events)
    event_id = input("ID события: ").strip()
    event = events.get(event_id)
    if event is None:
        print("Событие не найдено.")
        return

    guest_name = input("Имя гостя: ").strip()
    invitation = add_invitation(invitations, event_id, guest_name)
    event_date = date.fromisoformat(event["date"])
    text = create_invitation(event["name"], guest_name, event_date)
    print(f"Приглашение #{invitation['id']} создано:\n{text}")


def handle_menu_choice(
    choice: int,
    events: dict[str, dict[str, str]],
    invitations: list[dict[str, str]],
) -> bool:
    """Handle one menu command and return False when the user exits."""
    if choice == 0:
        return False
    if choice == 1:
        show_events(events)
    elif choice == 2:
        add_event_from_input(events)
    elif choice == 3:
        query = input("Название или часть названия: ")
        show_events(dict(find_events(events, query)))
    elif choice == 4:
        show_invitations(invitations)
    elif choice == 5:
        create_invitation_from_input(events, invitations)
    elif choice == 6:
        invitation_id = input("ID приглашения: ").strip()
        message = "Приглашение отменено."
        if not cancel_invitation(invitations, invitation_id):
            message = "Приглашение не найдено."
        print(message)
    elif choice == 7:
        invitation_id = input("ID приглашения: ").strip()
        response = input("Ответ гостя (да/нет/не знаю): ")
        if set_response(invitations, invitation_id, response):
            print(process_response(response))
        else:
            print("Приглашение не найдено.")
    elif choice == 8:
        query = input("Имя или часть имени гостя: ")
        show_invitations(find_invitations(invitations, query))
    elif choice == 9:
        print_statistics(invitations)
    else:
        print("Неизвестный пункт меню.")
    return True


def main() -> None:
    """Run the console application."""
    events = load_events()
    invitations = load_invitations()

    running = True
    while running:
        print(MENU)
        choice = input_int("Выберите пункт: ", minimum=0)
        try:
            running = handle_menu_choice(choice, events, invitations)
        except (ValueError, RuntimeError) as error:
            print(f"Ошибка: {error}")

        try:
            save_events(events)
            save_invitations(invitations)
        except RuntimeError as error:
            print(f"Ошибка сохранения: {error}")

    print("Данные сохранены. Работа завершена.")


if __name__ == "__main__":
    main()
