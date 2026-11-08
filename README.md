# Электронные приглашения — ПР9: модели Django и ORM

Продолжение [сквозного проекта](https://github.com/pkpal-uhobp/electronic-invitations) ПР1–ПР7. В ПР9 веб-слой переведён с `sqlite3` и ручных SQL-запросов на Django ORM без замены предметной области и пользовательских сценариев.

## Что изменилось в ПР9

- Созданы четыре модели Django: `users_web.User`, `guests_web.Guest`, `events_web.Event`, `invitations_web.Invitation`.
- Настроены `ForeignKey`, `related_name`, `on_delete` (`SET_NULL`/`CASCADE`), nullable FK, `DateField`, значения по умолчанию и `choices`.
- Добавлены начальные миграции во все четыре приложения. Структура **целевой** базы формируется `migrate`.
- Добавлена идемпотентная management-команда `import_pr7` для переноса из `data/invitations.sqlite` в Django `db.sqlite3` с сохранением ключей и связей. Исходная база остаётся неизменённой.
- Переписаны `views.py` всех пяти приложений: `Model.objects` вместо импорта `db.queries`/`db.repository`.
- Реализованы ORM-фильтры, `exclude`, `Q`, поиск по нескольким полям, белый список полей сортировки, `values`, `aggregate`, `annotate`, `Count`, `select_related` и `Paginator`.
- Сохранены страницы ПР6–ПР7: события, гости, организаторы, приглашения, подробности, поиск по дате, доступные гости, статистика и обработчики 400/403/404/500.
- Для приглашений добавлены поиск, фильтр по событию, сортировка, исключение отменённых и навигация с сохранением параметров запроса между страницами.
- Предыдущие консольные Python-модели в `models/`, JSON-хранилище, файлы `sql/`, `db/database.py`, `db/repository.py`, `db/queries.py` остаются как историческая реализация ПР1–ПР7. Они **не используются Django-представлениями ПР9**.
- Добавлены `tests/test_pr9_orm.py`, старые консольные и SQL smoke-тесты.

## Быстрый запуск (Windows)

Дважды щёлкните `RUN_WINDOWS.bat`, **или** в PowerShell из папки с `manage.py`:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py import_pr7
python manage.py check
python manage.py runserver
```

Приложение: http://127.0.0.1:8000/

По умолчанию включён режим разработки `DEBUG=True` для работы локальных CSS/JavaScript-файлов. Для проверки собственных страниц ошибок 400/403/404/500 установите `DJANGO_DEBUG=0` (при необходимости разрешите `localhost`/`127.0.0.1` через `DJANGO_ALLOWED_HOSTS`).

**Порядок важен:** сначала `migrate`, потом `import_pr7`. Команда `python -m db.import_json` требуется только для изменения / восстановления *исходной базы ПР7* на основе JSON. Она перезаписывает старые предметные таблицы и **не должна заменять** `import_pr7`.

Аналогично для Linux/macOS: `python3 -m venv .venv`, `source .venv/bin/activate`.

## Базы данных и перенос

| Путь | Назначение |
| --- | --- |
| `data/invitations.sqlite` | Исходная SQLite ПР7 (4 таблицы: `users`, `guests`, `events`, `invitations`) |
| `db.sqlite3` | Целевая БД Django с миграциями и моделями ORM (не входит в архив) |

Команда `python manage.py import_pr7 [--source /путь/к/старой.sqlite]` сначала читает источник только для чтения через `sqlite3`, затем в `transaction.atomic()` записывает объекты **исключительно через ORM**, в порядке `User` → `Guest` → `Event` → `Invitation`. Используется `update_or_create(pk=...)`. Повторный импорт не дублирует данные; существующие записи с теми же ID синхронизируются с источником, не удаляя записи, которые были добавлены только в Django. Перед импортом реальных данных сделайте резервную копию обеих баз.

Контрольные количества для вложенных демонстрационных данных: **2 организатора, 3 гостя, 2 события, 3 приглашения**. `event.date` из TEXT преобразуется в `date`.

## Схема моделей

| Модель | Поля | Обратная связь |
| --- | --- | --- |
| `users_web.User` | `name`, `email` | `user.events` |
| `guests_web.Guest` | `name`, `email` | `guest.invitations` |
| `events_web.Event` | `name`, `date`, `user` (`SET_NULL`, nullable) | `event.invitations` |
| `invitations_web.Invitation` | `event` (`CASCADE`), `guest` (`SET_NULL`, nullable), `guest_name`, `response`, `status` | — |

`users_web.User` — предметная модель *организатора*, не `django.contrib.auth.User`.

## Адреса страниц

- `/` — общие счётчики из ORM.
- `/events/`, `/events/<id>/` — события и детали; `q` и `sort` (дата, название, организатор).
- `/events/search/?date=2026-12-28` — поиск по дате (`filter(date=...)`).
- `/events/available/?event_id=1` — гости без **активного** приглашения на событие (подзапрос и `exclude`).
- `/invitations/`, `/invitations/<id>/` — приглашения и детали.
- `/invitations/?status=active&event_id=1&q=Анна&sort=date&page=1` — фильтры + многострочный поиск + безопасная сортировка + пагинация.
- `/invitations/?hide_cancelled=1` — демонстрация `exclude`.
- `/invitations/statistics/` — `aggregate`, `annotate`, `values`, `Count`; **включает события без приглашений и организаторов без событий**.
- `/users/`, `/users/<id>/` — организаторы и их связанные события.
- `/guests/`, `/guests/<id>/` — гости и их связанные приглашения.

Некорректные параметры дат/ID обрабатываются сообщениями, несуществующие объекты — 404, отсутствующие данные — пустыми состояниями в шаблонах. Поля сортировки сопоставлены со строгим белым списком.

## 15+ различных ORM-выражений из практической работы

Ниже перечислены **различные реально применяемые** выражения, а не 15 вызовов методов в одной цепочке:

| № | Где применяется | Пример ORM |
| ---: | --- | --- |
| 1 | Организаторы | `User.objects.all().order_by('name', 'pk')` |
| 2 | Гости | `Guest.objects.all().order_by('name', 'pk')` |
| 3 | События + организатор | `Event.objects.select_related('user')` |
| 4 | Поиск событий по названию / организатору | `Event.objects.filter(Q(name__icontains=q) \| Q(user__name__icontains=q))` |
| 5 | Детали события | `Event.objects.select_related('user').get(pk=...)` через `get_object_or_404` |
| 6 | События по дате | `Event.objects.filter(date=selected)` |
| 7 | Подзапрос активных приглашений | `Invitation.objects.filter(event_id=..., status='active').values('guest_id')` |
| 8 | Свободные гости | `Guest.objects.exclude(pk__in=invited_ids)` |
| 9 | Приглашения + связи | `Invitation.objects.select_related('event', 'guest', 'event__user')` |
| 10 | Приглашения по статусу | `Invitation.objects.filter(status=...)` |
| 11 | Исключение отменённых | `Invitation.objects.exclude(status='cancelled')` |
| 12 | Поиск по гостю / событию / почте | `Invitation.objects.filter(Q(...) \| Q(...) \| Q(...))` |
| 13 | Приглашения выбранного события | `Invitation.objects.filter(event_id=...)` |
| 14 | События организатора | `Event.objects.filter(user=user).select_related('user')` |
| 15 | Приглашения гостя | `Invitation.objects.filter(guest=guest).select_related(...)` |
| 16 | Сводка | `Invitation.objects.aggregate(total=Count('pk'), active=Count(...), ...)` |
| 17 | Статистика по событиям | `Event.objects.annotate(invitation_count=Count('invitations'), ...)` |
| 18 | Группировка по ответам | `Invitation.objects.values('response').annotate(invitation_count=Count('pk'))` |
| 19 | События по организаторам | `User.objects.annotate(event_count=Count('events'))` |
| 20 | Популярные события | `Event.objects.annotate(...).filter(invitation_count__gte=2)` |

Дополнительно есть сортировки по одному и нескольким полям (`order_by`) и отдельная пагинация `Paginator`. Создание, изменение, удаление и обратные связи демонстрируются в тестах `tests/test_pr9_orm.py` и Django Shell.

Пример Django Shell:

```python
from datetime import date
from events_web.models import Event
from guests_web.models import Guest
from invitations_web.models import Invitation
from users_web.models import User

organizer = User.objects.create(name='Тестовый организатор', email='test@example.com')
event = Event.objects.create(name='Тестовое мероприятие', date=date(2027, 1, 1), user=organizer)
guest = Guest.objects.create(name='Тестовый гость', email='guest@example.com')
invite = Invitation.objects.create(event=event, guest=guest, guest_name=guest.name)
invite.set_response('да')
invite.cancel()
print(organizer.events.all(), guest.invitations.all())
invite.delete()
event.delete()
guest.delete()
organizer.delete()
```

## Контрольные команды

```powershell
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py showmigrations
python manage.py test
pytest -v
flake8 . --extend-exclude=venv,.venv
```

`pytest-django` в `requirements.txt` нужен для использования изолированной тестовой базы. Прежние тесты ПР7/консольной версии также доступны.

## Контрольная точка Git (нужно выполнить в локальном клоне)

```powershell
git switch -c pr9-django-orm
git add .
git commit -m "PR9: модели Django, миграции и перенос данных"
```

Здесь предоставлен ZIP-каталог исходников, поэтому сам по себе архив **не содержит Git-истории и не создаёт коммит в GitHub**. При переносе в локальный клон сохраняйте собственный `.git`, копируйте файлы поверх клона и делайте осмысленные тематические коммиты с префиксом `PR9:`.

## Требования, не выполняемые автоматически

Прохождение 12 учебных тем Яндекс Практикума, демонстрация преподавателю и заполнение личных реквизитов отчёта являются самостоятельными действиями. Для них включены `docs/PR9_CHECKLIST.md` и `docs/PR9_REPORT_TEMPLATE.md`.
