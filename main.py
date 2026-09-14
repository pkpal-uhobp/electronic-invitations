from datetime import date


def check_event(name, event_date):
    """Проверяет корректность данных события."""
    if name == "":
        return False

    if event_date < date.today():
        return False

    return True


def create_invitation(event_name, guest_name, event_date):
    """Формирует электронное приглашение."""
    return (
        f"Здравствуйте, {guest_name}!\n"
        f"Приглашаем вас на событие «{event_name}».\n"
        f"Дата проведения: {event_date}."
    )


def process_response(response):
    """Обрабатывает ответ гостя."""
    if response == "да":
        return "Гость подтвердил участие."

    elif response == "нет":
        return "Гость отказался от участия."

    else:
        return "Ответ гостя пока не определён."


event_name = input("Введите название события: ")
guest_name = input("Введите имя гостя: ")

event_date = date(2026, 10, 15)

if check_event(event_name, event_date):
    invitation = create_invitation(
        event_name,
        guest_name,
        event_date
    )

    print("\nЭлектронное приглашение:")
    print(invitation)

    response = input("\nГость придёт? (да/нет/не знаю): ").lower()

    print(process_response(response))
else:
    print("Невозможно создать приглашение: проверьте данные события.")
