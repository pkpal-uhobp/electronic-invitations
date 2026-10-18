# Электронные приглашения — ПР6: шаблоны Django

Продолжение учебного проекта [pkpal-uhobp/electronic-invitations](https://github.com/pkpal-uhobp/electronic-invitations) после ПР5.

## Назначение

Система позволяет просматривать события, организаторов, гостей и электронные приглашения, а также их статусы и ответы. Предметная область осталась прежней:

- `User` — организатор; один организатор может создавать несколько `Event`;
- `Guest` — гость; один гость может иметь несколько `Invitation`;
- `Event` — событие; к одному событию относится несколько приглашений;
- `Invitation` — приглашение гостя на событие, статус `active/cancelled` и ответ `да/нет/не знаю`.

**Хранилище:** `data/*.json`. В ПР6 по-прежнему **не используются Django ORM и предметные модели базы**. SQLite применяется только для штатных механизмов Django (сессии, админка). Консольная версия запускается отдельно (`python main.py`). Веб-формы создания записей пока не реализованы.

## Возможности ПР6

- Шаблон `templates/base.html` с наследованием через `extends`, `block`.
- Общая навигация в `templates/includes/navigation.html` (через `include`).
- Отдельные шаблоны списков и подробных страниц всех четырёх сущностей.
- Общие карточки событий и приглашений через `include`.
- View-функции только загружают данные и используют `render(request, template, context)`.
- `for`, `empty`, `if`, фильтры `length`, `default`, `date` в шаблонах.
- Именованные пути и пространства имён (`homepage`, `events`, `invitations`, `users`, `guests`).
- Свой CSS, JavaScript (текущий год, меню на телефоне), PNG-логотип; подключение через `{% static %}`.
- 404 для отсутствующих идентификаторов и сохранение JSON-формата ПР5.
- Автотесты доменной логики и веб-маршрутов.

## Установка и запуск (Windows PowerShell)

Откройте терминал в корне `electronic-invitations-PR6` (там, где `manage.py`):

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py check
python manage.py runserver
```

Если PowerShell запрещает активацию, вместо неё можно выполнять команды через `.venv\Scripts\python.exe` непосредственно.

Linux/macOS: `python3 -m venv .venv`, затем `source .venv/bin/activate`.

Откройте сайт: http://127.0.0.1:8000/

## URL веб-части

| Адрес | Содержание |
| --- | --- |
| `/` | главная и статистика |
| `/events/` | события |
| `/events/1/` | отдельное событие |
| `/invitations/` | приглашения |
| `/invitations/1/` | отдельное приглашение |
| `/users/` | организаторы |
| `/users/1/` | отдельный организатор и события |
| `/guests/` | гости |
| `/guests/1/` | отдельный гость и приглашения |

Для несуществующих ID возвращается HTTP 404.

## Проверки

```powershell
python manage.py check
python manage.py test
pytest -q
```

`python manage.py test` — штатные тесты Django (набор pytest находится в `tests/`; поэтому проверку проекта выполняйте **`pytest -q`**).

## Структура

```text
electronic-invitations-PR6/
├── manage.py, main.py, events.py, invitations.py, users.py, guests.py
├── storage.py, utils.py, requirements.txt, README.md
├── models/                  # собственные классы Python (не ORM)
├── data/                    # events.json, invitations.json, users.json, guests.json
├── inviteweb/               # settings, urls, wsgi, asgi
├── templates/
│   ├── base.html
│   └── includes/navigation.html
├── homepage/
│   ├── templates/homepage/index.html
│   └── static/homepage/{css,js,img}/
├── events_web/templates/events_web/
│   ├── event_list.html, event_detail.html
│   └── includes/event_card.html
├── invitations_web/templates/invitations_web/
│   ├── invitation_list.html, invitation_detail.html
│   └── includes/{invitation_card,invitation_status}.html
├── users_web/templates/users_web/{user_list,user_detail}.html
├── guests_web/templates/guests_web/{guest_list,guest_detail}.html
└── tests/
```

## Важно для сдачи

Практическая №6 — **продолжение того же репозитория**, не новый репозиторий. Для сдачи перенесите изменения в исходный `electronic-invitations` и создайте коммит с префиксом `PR6:`. Этот ZIP — рабочая копия файлов без директории `.git`, сам по себе коммит в GitHub не создаёт.

```bash
git add .
git commit -m "PR6: transition to Django templates"
git push
```

### Отличия от ПР5

В ПР5 HTML генерировался через `HttpResponse(page(...))`, в ПР6 все пять приложений используют Django Template Language. Функция `page()` удалена из веб-слоя; JSON-хранилище и консольная часть сохранены.

## Критерии и результаты

Проверяйте пункты чек-листа ПР6 из методички: корректность маршрутов, открытие списков и деталей, пустые списки, 404, `extends`, `include`, `block`, `static`, README, Git и демонстрация проекта.
