from datetime import date

def input_int(prompt: str, minimum: int | None = None) -> int:
    while True:
        try:
            value = int(input(prompt))
            if minimum is not None and value < minimum:
                raise ValueError
            return value
        except ValueError:
            print('Введите корректное целое число.')

def input_date(prompt: str) -> date:
    while True:
        try:
            return date.fromisoformat(input(prompt).strip())
        except ValueError:
            print('Введите дату в формате ГГГГ-ММ-ДД.')
