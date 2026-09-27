"""Консольное меню проекта."""

from datetime import date

from storage import (
    load_events,
    load_invitations,
    save_events,
    save_invitations
)

from events import add_event, sort_events
from invitations import add_invitation


def print_menu():
    print("\nЭлектронные приглашения")
    print("1. Показать события")
    print("2. Создать событие")
    print("3. Создать приглашение")
    print("4. Показать приглашения")
    print("0. Выход")


def main() -> None:
    events = load_events()
    invitations = load_invitations(events)

    while True:
        print_menu()

        choice = input("Выберите действие: ")

        if choice == "1":
            print("\nСписок событий:")
            for event in sort_events(events):
                print(event)

        elif choice == "2":
            name = input("Название события: ")

            event = add_event(
                events,
                name,
                date.today()
            )

            print("Событие создано:")
            print(event)

        elif choice == "3":
            if not events:
                print("Сначала создайте событие!")
                continue

            print("Выберите событие:")

            for index, event in enumerate(events):
                print(index, event)

            index = int(input("Номер события: "))

            guest = input("Имя гостя: ")

            invitation = add_invitation(
                invitations,
                events[index],
                guest
            )

            print("Приглашение создано:")
            print(invitation)

        elif choice == "4":
            print("\nПриглашения:")
            for invitation in invitations:
                print(invitation)

        elif choice == "0":
            save_events(events)
            save_invitations(invitations)

            print("Данные сохранены. Выход.")
            break

        else:
            print("Такого пункта нет!")


if __name__ == "__main__":
    main()