"""Консольное меню проекта, сохранённое после ПР3."""

from datetime import date

from events import add_event, sort_events
from invitations import add_invitation
from storage import (
    load_events,
    load_guests,
    load_invitations,
    load_users,
    save_events,
    save_guests,
    save_invitations,
    save_users,
)


def print_menu() -> None:
    """Показать пункты консольного меню."""
    print("\nЭлектронные приглашения")
    print("1. Показать события")
    print("2. Создать событие")
    print("3. Создать приглашение")
    print("4. Показать приглашения")
    print("5. Показать пользователей")
    print("6. Показать гостей")
    print("0. Выход")


def main() -> None:
    """Запустить консольную версию приложения."""
    users = load_users()
    guests = load_guests()
    events = load_events(users)
    invitations = load_invitations(events, guests)

    while True:
        print_menu()
        choice = input("Выберите действие: ")

        if choice == "1":
            print("\nСписок событий:")
            for event in sort_events(events):
                organizer = event.user.name if event.user else "не указан"
                print(f"{event} | организатор: {organizer}")

        elif choice == "2":
            name = input("Название события: ")
            user = users[0] if users else None
            event = add_event(events, name, date.today(), user)
            print("Событие создано:")
            print(event)

        elif choice == "3":
            if not events:
                print("Сначала создайте событие!")
                continue
            if not guests:
                print("В data/guests.json нет гостей.")
                continue

            print("Выберите событие:")
            for index, event in enumerate(events):
                print(index, event)
            event_index = int(input("Номер события: "))

            print("Выберите гостя:")
            for index, guest in enumerate(guests):
                print(index, guest)
            guest_index = int(input("Номер гостя: "))

            invitation = add_invitation(
                invitations,
                events[event_index],
                guests[guest_index],
            )
            print("Приглашение создано:")
            print(invitation)

        elif choice == "4":
            print("\nПриглашения:")
            for invitation in invitations:
                print(invitation)

        elif choice == "5":
            print("\nПользователи:")
            for user in users:
                print(user)

        elif choice == "6":
            print("\nГости:")
            for guest in guests:
                print(guest)

        elif choice == "0":
            save_users(users)
            save_guests(guests)
            save_events(events)
            save_invitations(invitations)
            print("Данные сохранены. Выход.")
            break

        else:
            print("Такого пункта нет!")


if __name__ == "__main__":
    main()
