"""Консольная версия (ПР3), сохранена параллельно с Django."""
from datetime import date
from events import add_event, sort_events
from invitations import add_invitation
from storage import (load_events, load_guests, load_invitations, load_users,
                     save_events, save_guests, save_invitations, save_users)

def main():
    users = load_users(); guests = load_guests()
    events = load_events(users); invitations = load_invitations(events, guests)
    while True:
        print('\nЭлектронные приглашения — консольная версия')
        print('1. События  2. Добавить событие  3. Пригласить  4. Приглашения')
        print('5. Пользователи  6. Гости  0. Выход')
        choice = input('Пункт меню: ').strip()
        if choice == '1':
            for event in sort_events(events): print(event)
        elif choice == '2':
            try:
                event = add_event(events, input('Название: '), date.fromisoformat(input('Дата ГГГГ-ММ-ДД: ')), users[0] if users else None)
                print('Создано:', event)
            except ValueError as exc: print('Ошибка:', exc)
        elif choice == '3':
            if not events or not guests:
                print('Необходимы события и гости'); continue
            for n,e in enumerate(events): print(n,e)
            try:
                e = events[int(input('Номер события: '))]
                for n,g in enumerate(guests): print(n,g)
                g = guests[int(input('Номер гостя: '))]
                print('Создано:', add_invitation(invitations,e,g))
            except (IndexError,ValueError) as exc: print('Ошибка:',exc)
        elif choice == '4':
            for invitation in invitations: print(invitation)
        elif choice == '5':
            for user in users: print(user)
        elif choice == '6':
            for guest in guests: print(guest)
        elif choice == '0':
            save_users(users); save_guests(guests)
            save_events(events); save_invitations(invitations)
            print('Данные сохранены.'); break
        else: print('Нет такого пункта')

if __name__ == '__main__': main()
