# Электронные приглашения — практическая работа №10

**Продолжение ПР9 в том же Django-проекте**. Код построен на GitHub-версии ПР9, коммит [`2b180d7`](https://github.com/pkpal-uhobp/electronic-invitations/commit/2b180d7de61da599afcc66ca345104675be56a3b), ветка `main`. Предметная область не меняется: `User` (организатор), `Guest` (гость), `Event` (событие), `Invitation` (приглашение). Исходные консольные и SQL-модули сохранены.

## Что реализовано в ПР10

| Возможность | Файлы |
| --- | --- |
| Русскоязычная Django Admin с `list_display`, `search_fields`, `list_filter`, `ordering`, `list_per_page`, `autocomplete_fields` | `events_web/admin.py`, `users_web/admin.py`, `guests_web/admin.py`, `invitations_web/admin.py` |
| Списки связанных приглашений внутри события и гостя, события у организатора | классы `TabularInline` внутри `admin.py` |
| Русскоязычные имена приложений и полей | `*/apps.py`, `*/models.py` и новые миграции |
| `TextChoices`: `active`/`cancelled`/`completed`, методы QuerySet `active()`, `cancelled()`, `completed()`, `for_event()` | `invitations_web/models.py`, `0002_invitation_status_manager.py` |
| Ограничение повторного активного приглашения одному гостю на событие | `Invitation.clean`, условный `UniqueConstraint` для ненулевого `guest_id`; для гостя без FK сравнение имён через `casefold()` (кириллица в SQLite `iexact` не сравнивается по регистру) |
| Генерируемое БД поле `name_length` | `events_web/models.py`, `0004_event_name_length.py` |
| Читаемые транслитерированные URL событий, автоматическое заполнение slug, `get_absolute_url` | `events_web/models.py`, `events_web/views.py`, `events_web/urls.py`, миграции `0002` и `0003` |
| Общие данные в шаблонах | `events_web/context_processors.py`, `inviteweb/settings.py`, `templates/includes/navigation.html` |
| SQL-инструменты | Django Debug Toolbar при `DEBUG=1`, команда `pr10_sql_report` |
| ORM `F`, `values`, `annotate`, оптимизация связей, статусная статистика | `invitations_web/views.py`, `events_web/views.py`, шаблоны |
| Новые регрессионные тесты | `tests/test_pr10_admin.py` |

### Схема и сохраняемые связи

`User` 1—N `Event` (`SET_NULL` при удалении организатора). `Event` 1—N `Invitation` (`CASCADE` при удалении события). `Guest` 1—N `Invitation` (`SET_NULL` при удалении гостя). Вход в `/admin/` осуществляется через **стандартную учётную запись Django**, не через предметную модель `users_web.User`.

Новый статус `completed` задаётся вручную, **не автоматически по дате**. В списке доступных гостей учитываются только `active`: завершённые и отменённые не блокируют приглашение.

### URL событий

- `/events/` — общий список, поиск и сортировка.
- `/events/den-rozhdeniia-1/` — предпочитаемая страница по латинскому slug (конкретное значение зависит от имени и ID).
- `/events/1/` — старый URL из ПР9, оставлен рабочим для существующих ссылок и тестов.
- `/events/search/`, `/events/available/` — прежние сценарии сохранены.
- `/invitations/?status=completed` — фильтр нового статуса.
- `/invitations/statistics/` — статистика, включая завершённые и `F`/`values()`.
- `/admin/` — Django Admin.
- `/__debug__/` — SQL Debug Toolbar **только при `DEBUG=1`**.

### Быстрый запуск на Windows

1. Сохранить/скопировать старую `db.sqlite3`. Никогда не удалять её ради обновления.
2. В папке проекта дважды щёлкнуть `RUN_WINDOWS.bat` — он устанавливает пакеты, выполняет `migrate`, импортирует ПР7 **только в пустую базу**, запускает сервер в отладочном режиме.
3. Для входа в `/admin/` один раз выполнить:

```powershell
.\.venv\Scripts\python.exe manage.py createsuperuser
```

Проверить: http://127.0.0.1:8000/admin/ . Полные инструкции — [`docs/PR10_RUN_GUIDE.md`](docs/PR10_RUN_GUIDE.md).

### Проверка качества и SQL

```powershell
$env:DJANGO_DEBUG = '1'
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py makemigrations --check --dry-run
.\.venv\Scripts\python.exe manage.py showmigrations
.\.venv\Scripts\python.exe -m pytest -v
.\.venv\Scripts\python.exe -m flake8 . --extend-exclude=venv,.venv
.\.venv\Scripts\python.exe manage.py pr10_sql_report --show-sql
```

Реальное количество SQL-запросов зависит от наполнения базы и выбранных GET-параметров; не задавайте его заранее. Для отчёта снимите **настоящие** скриншоты Django Admin, Debug Toolbar SQL и терминала с тестами.

### Миграции

В ПР9 уже было `Invitation.status` (`active`, `cancelled`), а отдельного поля `is_cancelled` не было: в ПР10 расширяем существующее поле до `TextChoices` и добавляем `completed`, без фиктивной миграции `is_cancelled`. Новые `Event.slug`, данные slug для старых событий и `GeneratedField` находятся в последовательных миграциях `0002–0004`; прежняя `0001_initial.py` не менялась.

**SQLite**: у `Event.name_length` `GeneratedField(db_persist=False)` — виртуальный вычисляемый столбец. Это адаптация к SQLite в уже заполненном проекте. Меняя `Event.name`, после `save()` выполните `refresh_from_db()` для чтения нового значения.

### Исторические части проекта

`models/`, `events.py`, `users.py`, `guests.py`, `invitations.py`, `storage.py`, `main.py`, `data/*.json`, `data/invitations.sqlite`, `db/`, `sql/` — прежняя учебная консольная и SQL-версия. Django-web слой работает с `db.sqlite3` через ORM; файл `db.sqlite3` игнорируется Git.

### Сдача

- [`docs/PR10_CHECKLIST.md`](docs/PR10_CHECKLIST.md): подробный список реализованного и того, что нужно проверить локально.
- [`docs/PR10_REPORT_TEMPLATE.md`](docs/PR10_REPORT_TEMPLATE.md): структура отчёта по методичке, без вымышленных скриншотов и статуса выполнения онлайн-курса.
- [`docs/PR10_RUN_GUIDE.md`](docs/PR10_RUN_GUIDE.md): перенос поверх существующего Git, запуск, тестирование.

**GitHub автоматически не изменён**: архив — исходники, коммиты `PR10:` и `git push` необходимо выполнить в вашем локальном клоне. Три блока Яндекс Практикума и фактическую проверку Django Admin в браузере также нужно пройти лично.
