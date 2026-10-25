# Электронные приглашения — ПР6 + ПР7

Продолжение сквозного учебного проекта: [pkpal-uhobp/electronic-invitations](https://github.com/pkpal-uhobp/electronic-invitations).

## Назначение

Просмотр событий, организаторов, гостей, электронных приглашений, ответов и статусов. Предметные Python-модели `User`, `Guest`, `Event`, `Invitation` и консольная версия проекта сохранены.

## ПР6: Django Templates

- Общий шаблон `templates/base.html`, блоки `{% block %}` и наследование `{% extends %}`.
- Подключаемые компоненты: навигация, карточки событий и приглашений, статус приглашения.
- View-функции вызывают `render()` и передают данные в контекст.
- Именованные маршруты с пространствами имён: `homepage`, `events`, `invitations`, `users`, `guests`.
- Условия, циклы и фильтры `length`, `date`, `default` в шаблонах.
- Собственные CSS, JavaScript и PNG-логотип подключены через `{% static %}`.
- Кастомные шаблоны ошибок HTTP 400, 403, 404, 500 — с правильными кодами ответа. В Django они автоматически используются при `DEBUG=False`.

## ПР7: SQLite + SQL (без Django ORM)

**Предметная БД:** `data/invitations.sqlite`. Django сохраняет собственную служебную БД `db.sqlite3` для auth/admin — она не является частью SQL-задания.

| Таблица | Поля | Связи |
| --- | --- | --- |
| `users` | `id INTEGER PRIMARY KEY`, `name TEXT`, `email TEXT` | организаторы |
| `guests` | `id INTEGER PRIMARY KEY`, `name TEXT`, `email TEXT` | гости |
| `events` | `id INTEGER PRIMARY KEY`, `name TEXT`, `date TEXT`, `user_id INTEGER` | `user_id → users.id`, допускает NULL |
| `invitations` | `id INTEGER PRIMARY KEY`, `event_id INTEGER`, `guest_id INTEGER`, `guest_name TEXT`, `response TEXT`, `status TEXT` | `event_id → events.id`, `guest_id → guests.id` |

Схема создаётся из `sql/schema.sql`. В `db/database.py` используются `sqlite3.connect()`, `PRAGMA foreign_keys=ON` и `sqlite3.Row`. В `db/import_json.py` реализован импорт через `executemany()` с параметрами `?` и транзакцией `commit` (контекстный менеджер соединения). Повторный запуск импорта безопасен: синхронизирует предметные таблицы с исходными JSON, не создавая дубликаты. **Импорт перезаписывает четыре предметные таблицы**, поэтому изменения, внесённые непосредственно в SQLite, до повторного импорта нужно сохранить отдельно.

В `sql/queries.sql` находятся **19 именованных SQL-запросов**, все читаются из Django через `db/queries.py`:

- `SELECT`: `users_list`, `guests_list`, `events_list`, `invitations_list`;
- `WHERE`: `event_by_id`, `invitation_by_id`, `user_by_id`, `guest_by_id`, `events_on_date`, `invitations_by_status`, `invitations_for_guest`, `events_for_user`;
- `JOIN`: `events_list`, `invitations_list`, `event_by_id`, `invitation_by_id` и другие;
- агрегаты `COUNT`, `SUM`: `total_counts`, `invitation_totals`;
- `GROUP BY`: `invitations_by_event`, `invitations_by_response`, `organizer_event_counts`, `popular_events` (с `HAVING`).

Запросы с пользовательским вводом всегда параметризованы. SQL выполняется в `sqlite3`, а результат передаётся в Django через контекст `render()`; ORM предметной области не используется. JSON-файлы и консольные команды из предыдущих практических **сохранены**.

## Установка и запуск (Windows PowerShell)

Из корня проекта, где находится `manage.py`:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m db.import_json
python manage.py migrate
python manage.py check
python manage.py runserver
```

Для Linux/macOS используйте `python3 -m venv .venv` и `source .venv/bin/activate`.

База `data/invitations.sqlite` прилагается с примером исходных данных, однако команду `python -m db.import_json` рекомендуется выполнить для гарантированной синхронизации с JSON. Для обновления данных после редактирования JSON снова запустите эту команду.

## URL-страницы

| Адрес | Назначение | Источник данных |
| --- | --- | --- |
| `/` | Главная и сводные показатели | SQLite `total_counts` |
| `/events/`, `/events/1/` | События и детали | SQLite + JOIN |
| `/events/search/?date=2026-12-28` | Поиск событий по дате | SQL `WHERE` |
| `/events/available/?event_id=1` | Гости, у которых ещё нет активного приглашения | `NOT EXISTS`, параметризованный SQL |
| `/invitations/`, `/invitations/1/` | Приглашения и детали | SQLite + JOIN |
| `/invitations/?status=active` | Фильтрация приглашений | SQL `WHERE` |
| `/invitations/statistics/` | Число приглашений, ответы, статистика по событиям и организаторам | `COUNT`, `SUM`, `GROUP BY`, `HAVING` |
| `/users/`, `/users/1/` | Организаторы и их события | SQLite + JOIN |
| `/guests/`, `/guests/1/` | Гости и их приглашения | SQLite + JOIN |

### Страницы ошибок

В `inviteweb/urls.py` назначены `handler400`, `handler403`, `handler404`, `handler500`. Используются отдельные шаблоны `templates/400.html`, `403.html`, `404.html`, `500.html` и общий компонент `templates/errors/error_panel.html`.

Для проверки 404 в рабочем режиме отключите отладку:

```powershell
$env:DJANGO_DEBUG='0'
$env:DJANGO_ALLOWED_HOSTS='127.0.0.1,localhost,testserver'
python manage.py runserver
```

Откройте, например, `http://127.0.0.1:8000/events/999/` или `http://127.0.0.1:8000/no-such-page/`. Остальные обработчики проверяются тестами; публичные маршруты для искусственного вызова серверных ошибок не добавляются.

## Проверки

```powershell
python manage.py check
pytest -q
flake8 . --extend-exclude=venv,.venv
```

SQL-запросы вручную можно выполнить в SQLite CLI: `sqlite3 data/invitations.sqlite`, затем `.read sql/queries.sql`. **Обратите внимание:** именованные запросы с `?` требуют передачи параметра в Python; их удобнее проверять через автотесты или выполнить вручную с конкретным значением.

## Структура нового слоя

```text
db/
  __init__.py
  database.py              # sqlite3 + sqlite3.Row + PRAGMA
  import_json.py            # импорт JSON → SQLite
  queries.py                # читает именованные SQL из SQL-файла
  repository.py             # адаптирует sqlite3.Row для старых шаблонов
sql/
  schema.sql                # 4 таблицы + индексы + FK
  queries.sql               # 19 SQL-запросов
data/
  invitations.sqlite        # готовая предметная база
  events.json, users.json, guests.json, invitations.json # исходный ПР6
inviteweb/error_views.py   # custom 400/403/404/500
templates/400.html, 403.html, 404.html, 500.html
templates/errors/error_panel.html
events_web/templates/events_web/event_search.html
events_web/templates/events_web/available_guests.html
invitations_web/templates/invitations_web/statistics.html
homepage/static/homepage/css/pr7.css
tests/test_pr7_sql.py
```

ПР7 выполняется в **том же репозитории**; для тематических коммитов используйте префикс `PR7:`. Для внесения изменений в GitHub нужна роль с правом Push в репозиторий.
