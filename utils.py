"""Вспомогательные функции безопасного консольного ввода."""

from datetime import date


def input_int(prompt: str, minimum: int | None = None) -> int:
    """Считать целое число и повторять запрос после неверного ввода."""
    while True:
        try:
            value = int(input(prompt))
            if minimum is not None and value < minimum:
                raise ValueError
            return value
        except ValueError:
            print("Введите корректное целое число.")


def input_date(prompt: str) -> date:
    """Считать дату в формате YYYY-MM-DD."""
    while True:
        raw_value = input(prompt).strip()
        try:
            return date.fromisoformat(raw_value)
        except ValueError:
            print("Введите дату в формате ГГГГ-ММ-ДД.")
