# Запуск ПР10 на Windows (в существующем Git-клоне)

## Безопасный перенос поверх ПР9

1. Проверьте `git status`. Если есть важные незакоммиченные изменения, зафиксируйте или сохраните их.
2. Сделайте копию `db.sqlite3`, например `db.sqlite3.backup`, **вне каталога проекта**. Никогда не удаляйте текущую базу ради миграций.
3. Распакуйте ZIP в **временную папку**, затем перенесите файлы в папку своего Git-клона, сохранив `.git/`, `.venv/` и `db.sqlite3`. Не копируйте из старых архивов бинарные `__pycache__`.
4. Перенос **не изменяет GitHub** автоматически: после проверок сделайте коммиты и `git push` самостоятельно.

## Автоматический запуск

`RUN_WINDOWS.bat` создаст окружение при необходимости, установит зависимости, применит миграции, импортирует ПР7 **только в пустые предметные таблицы**, проверит Django и запустит сервер с `DJANGO_DEBUG=1`.

Если `db.sqlite3` уже содержит предметные данные ПР9, они не перезаписываются. Админ-доступ нужно создать вручную один раз:

```powershell
.\.venv\Scripts\python.exe manage.py createsuperuser
```

Сайт: http://127.0.0.1:8000/ , админ: http://127.0.0.1:8000/admin/ .

## Ручные команды (PowerShell)

```powershell
$env:DJANGO_DEBUG = '1'
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py import_pr7_if_empty
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py showmigrations
.\.venv\Scripts\python.exe manage.py makemigrations --check --dry-run
.\.venv\Scripts\python.exe -m pytest -v
.\.venv\Scripts\python.exe -m flake8 . --extend-exclude=venv,.venv
.\.venv\Scripts\python.exe manage.py pr10_sql_report --show-sql
.\.venv\Scripts\python.exe manage.py createsuperuser
.\.venv\Scripts\python.exe manage.py runserver
```

Если `createsuperuser` уже был выполнен, повторно создавать пользователя не нужно.

## Проверки вручную

- `/admin/`: модели Event, Invitation, User, Guest; поиски и фильтры; редактирование статуса; inline-формы.
- `/events/`: ссылка события в виде `/events/den-rozhdeniia-1/`; старая `/events/1/` продолжает работать.
- `/invitations/`: фильтр `status=completed`; условия, сортировка, переходы страниц.
- `/events/available/?event_id=1`: только активное приглашение блокирует гостя.
- `/invitations/statistics/`: счётчик завершённых и данные `annotate(F(...))`.
- Django Debug Toolbar (при `DJANGO_DEBUG=1`) — вкладка `SQL` на HTML-страницах.

## Действия в Git

```powershell
git status
git diff
git add -A
git diff --cached --stat
git commit -m "PR10: админ-панель, статусы и ORM-оптимизация"
git push origin main
```

Не выполняйте `git add -A`, пока не проверили `git status`. Репозиторий ПР9 содержит ошибочно отслеживаемые `*.pyc`; их стоит исключить из индекса отдельно, но не удалять пользовательские файлы и базы.

## Режим выпуска

По умолчанию в исходных настройках `DJANGO_DEBUG=0`, что соответствует вашему GitHub после ПР9. Для локальной проверки Django Admin и SQL используйте `DJANGO_DEBUG=1`, как в `RUN_WINDOWS.bat`. Django Debug Toolbar **не подключается** в `DEBUG=False`. Настоящая публикация требует WSGI/ASGI-сервера, HTTPS, постоянного `DJANGO_SECRET_KEY` и настроенной раздачи статики; `runserver` для неё не предназначен.
