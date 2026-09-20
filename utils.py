"""Input helpers with exception handling."""

from datetime import date


def input_int(prompt: str, minimum: int | None = None) -> int:
    """Read an integer and repeat the prompt after invalid input."""
    while True:
        try:
            value = int(input(prompt))
            if minimum is not None and value < minimum:
                raise ValueError
            return value
        except ValueError:
            print("Введите корректное целое число.")


def input_date(prompt: str) -> date:
    """Read a date in YYYY-MM-DD format."""
    while True:
        raw_value = input(prompt).strip()
        try:
            return date.fromisoformat(raw_value)
        except ValueError:
            print("Введите дату в формате ГГГГ-ММ-ДД.")
