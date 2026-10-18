# Практическая работа № 6 — ответы на 25 вопросов для защиты

**Проект:** «Электронные приглашения» (`electronic-invitations-PR6`).  
**Основа:** методичка «ПР6. Шаблоны Django и проектная разработка», пункты 1–25 таблицы оценивания (стр. 56–57), и **реальные исходные файлы этого архива**.  
**Важная адаптация:** в методичке иллюстрации даны на Roomly (помещения `Room` и бронирования `Booking`). В индивидуальном проекте вместо них используются `Event` (событие), `Invitation` (приглашение), `Guest` (гость) и `User` (организатор). «Отмена бронирования» здесь соответствует `invitation.status == 'cancelled'`. Поля `is_cancelled` в нашем классе `Invitation` нет. В ПР6 источник данных — **JSON**, а не Django ORM.

## Как показывать работу на защите

1. В терминале из корня проекта (рядом с `manage.py`): `python manage.py runserver`.
2. В браузере откройте `http://127.0.0.1:8000/`, `/events/`, `/events/1/`, `/invitations/`, `/invitations/1/`. Демонстрационные данные находятся в `data/*.json`.
3. Покажите названный в каждом ответе файл и нужный фрагмент. Для требуемого эксперимента **временно** измените код или данные, обновите браузер, объясните результат, после чего **верните исходное значение**. Эксперименты ниже не внесены в рабочие файлы проекта специально, чтобы не ломать сдаваемую версию.
4. При проблемах с загрузкой: `python manage.py check`; для тестов: `pytest -q` (потребуются зависимости из `requirements.txt`).

---

## 1. Наследование шаблонов

**Где показать:** `templates/base.html` и `events_web/templates/events_web/event_list.html` (либо `homepage/templates/homepage/index.html`).

В базовом шаблоне есть общие HTML, меню, стили и точка для дочернего содержимого:

```django
<title>{% block title %}{{ page_title|default:"Главная" }} — Электронные приглашения{% endblock %}</title>
<main class="container main-content">
  {% block content %}{% endblock %}
</main>
```

В дочерней странице реально стоит `{% extends 'base.html' %}`. Он велит Django построить страницу по каркасу `base.html`, подставляя переопределённые блоки. Например, **временно** добавьте в `event_list.html` сразу после `extends`:

```django
{% block title %}Список моих событий — ПР6{% endblock %}
```

**Что увидим:** заголовок вкладки `/events/` станет «Список моих событий — ПР6», а меню и остальные части базовой страницы сохранятся. Заголовок не изменяется во всех страницах, только в этой дочерней.

## 2. Переопределение блоков `title` и `content`

**Где показать:** `templates/base.html` и `homepage/templates/homepage/index.html`.

Главная страница уже переопределяет оба блока:

```django
{% extends 'base.html' %}
{% block title %}Главная — Электронные приглашения{% endblock %}
{% block content %}
<section class="hero"> ... </section>
{% endblock %}
```

**Демонстрация:** временно замените в `block content` заголовок `<h1>` на `Тест защиты ПР6`. При обновлении `/` надпись поменяется, потому что содержимое дочернего блока подставляется в место `{% block content %}` родителя. Верните исходный заголовок.

## 3. Передача контекста из `render()`

**Где показать:** `events_web/views.py`, функция `events()`; `events_web/templates/events_web/event_list.html`.

```python
def events(request):
    event_list = sort_events(load_events())
    return render(request, 'events_web/event_list.html', {
        'page_title': 'События', 'events': event_list,
    })
```

Шаблон обращается к ключу `events` через `{% for event in events %}` и `{{ events|length }}`. **Эксперимент:** поменяйте ключ в `render()` с `'events'` на `'items'`, но шаблон оставьте прежним. Результат: список окажется пустым, в цикле сработает `{% empty %}`, счётчик потеряет исходное значение. Причина — переменной `events` теперь нет в контексте. Исправление: вернуть `'events'` или одновременно обновить шаблон, используя `items`.

## 4. Обращение к атрибутам объектов

**Где показать:** `events_web/templates/events_web/includes/event_card.html` и `models/events.py`.

Реальный код карточки:

```django
<h2>{{ event.name|default:'Без названия' }}</h2>
<span class="date-label">{{ event.date }}</span>
```

`event` — Python-объект `Event`, в котором есть атрибуты `id`, `name`, `date`, `user`. **Эксперимент:** временно укажите `{{ event.title }}` вместо `{{ event.name }}`. В классе нет поля `title`, поэтому Django обычно отобразит пустое место (при стандартном `string_if_invalid=''`), а не текст названия. Ошибка может быть незаметной — нужно сверять атрибуты с `models/events.py`.

## 5. Обработка отсутствующих переменных

**Где показать:** любой дочерний шаблон, например `events_web/templates/events_web/event_detail.html`.

Добавьте на время:

```django
<p>Проверка: [{{ missing_variable }}]</p>
```

**Результат:** видим «Проверка: []». Движок шаблонов по умолчанию подставляет пустую строку для отсутствующей переменной. Это удобно для необязательных данных, но усложняет отладку опечаток: неверное имя может «молчать». Проверяйте ключи в словаре `context` и правильность имён переменных в шаблоне. После демонстрации строку удалите.

## 6. Автоматическое экранирование HTML

**Где показать:** `events_web/templates/events_web/event_detail.html`, где уже выводится `{{ event.name }}`; исходные значения лежат в `data/events.json`.

Предположим, в поле `name` у события временно хранится `<b>Вечеринка</b>`. Вывод через `{{ event.name }}` покажет **буквально** символы `<b>Вечеринка</b>`, а не жирный HTML-текст: Django экранирует пользовательские данные (`<` превращается в `&lt;`, и т.д.).

**Опасность:** `{{ event.name|safe }}` или `{% autoescape off %}` доверяют тексту как HTML. Если в JSON попадёт пользовательский `<script>…</script>` или обработчик события, возможна XSS-атака. Не отключайте автоэкранирование для недоверенных данных. После опыта восстановите JSON.

## 7. Обработка коллекций, `{% for %}` и `{% empty %}`

**Где показать:** `events_web/templates/events_web/event_list.html`:

```django
{% for event in events %}
  {% include 'events_web/includes/event_card.html' %}
{% empty %}
  <div class="empty-state">Пока нет событий...</div>
{% endfor %}
```

**Демонстрация:** временно присвойте `event_list = []` перед `render()` в `events_web/views.py`. После перезагрузки `/events/` карточки исчезнут, появится сообщение из ветки `{% empty %}`. Затем верните исходную загрузку. Это позволяет делать корректные страницы даже при отсутствии данных.

## 8. Условное отображение статуса

**Где показать:** `invitations_web/templates/invitations_web/includes/invitation_status.html`:

```django
{% if invitation.status == 'cancelled' %}
  <span class="status-pill status-muted">Отменено</span>
{% else %}
  <span class="status-pill status-active">Активно</span>
{% endif %}
```

У `Invitation` в этом проекте **нет** `is_cancelled`; используется строковое поле `status`. **Демонстрация:** в `data/invitations.json` у приглашения с `id="1"` временно поменяйте `"status": "active"` на `"status": "cancelled"`, затем обновите `/invitations/1/`. Значок поменяется с «Активно» на «Отменено». Верните `active`.

## 9. Фильтры шаблонов

**Где показать:** `events_web/templates/events_web/event_list.html` и `events_web/templates/events_web/event_detail.html`.

В проекте применены:

```django
{{ events|length }}
{{ event_date|date:'d.m.Y' }}
{{ event.name|default:'Без названия' }}
```

`length` показывает число элементов, `date` форматирует дату, `default` заменяет отсутствующее или ложное значение. **Демонстрация:** временно поменяйте название в карточке на `{{ event.name|upper }}` — оно станет прописными буквами. Можно комбинировать фильтры, например `{{ event.name|default:'Без названия'|upper }}`. После объяснения верните первоначальный вывод.

## 10. Обработка пустых значений через `default`

**Где показать:** `events_web/templates/events_web/includes/event_card.html`.

```django
<h2>{{ event.name|default:'Без названия' }}</h2>
```

**Эксперимент:** передайте в контексте `event.name = ''` (временно, для демонстрации; лучше не сохранять повреждённые JSON-данные). Вместо пустого заголовка появится «Без названия». Фильтр `default` подменяет значение, если оно отсутствует либо воспринимается как ложное (`''`, `None`, `False`, `0`). Для замены только `None` можно использовать `default_if_none`. Верните исходное значение.

## 11. Повторное использование шаблонов через `include`

**Где показать:** `templates/base.html`, `templates/includes/navigation.html`, `invitations_web/templates/invitations_web/includes/invitation_status.html`.

В `base.html`:

```django
{% include 'includes/navigation.html' %}
```

В шаблонах списка и отдельного приглашения используется:

```django
{% include 'invitations_web/includes/invitation_status.html' %}
```

**Демонстрация:** временно замените в `invitation_status.html` подпись «Активно» на «Подтверждено». На `/invitations/` и `/invitations/1/` подпись изменится сразу, потому что обе страницы подгружают один фрагмент. Верните исходный текст.

## 12. Передача данных во включаемый шаблон

**Где показать:** `events_web/templates/events_web/event_list.html` и `events_web/templates/events_web/includes/event_card.html`.

В родительском шаблоне переменная `event` создаётся циклом и доступна включаемой карточке:

```django
{% for event in events %}
    {% include 'events_web/includes/event_card.html' %}
{% endfor %}
```

В карточке: `{{ event.name }}`, `{{ event.id }}`. **Эксперимент:** временно переименуйте переменную цикла в `item`, но оставьте `event_card.html` без изменений. Карточка утратит данные из `event`, потому что переменная больше не передаётся под этим именем. **Корректный вариант явной передачи:**

```django
{% for item in events %}
  {% include 'events_web/includes/event_card.html' with event=item %}
{% endfor %}
```

Здесь `event` во фрагменте снова указывает на объект `item`.

## 13. Динамические URL через `{% url %}`

**Где показать:** `events_web/templates/events_web/includes/event_card.html` и `events_web/urls.py`.

```django
<a href="{% url 'events:detail' event.id %}">Подробнее</a>
```

Маршрут `events:detail` получает числовой ID. Для карточки события с `id=1` Django построит `/events/1/`, а с `id=2` — `/events/2/`. **Эксперимент:** во временной копии карточки используйте `{% url 'events:detail' 2 %}`; ссылка будет вести на `/events/2/`, даже если подпись первой карточки осталась прежней. Такой фиксированный ID не надо оставлять в финальной версии.

## 14. Пространства имён маршрутов

**Где показать:** `events_web/urls.py`, `inviteweb/urls.py`, `templates/includes/navigation.html`.

```python
# events_web/urls.py
app_name = 'events'
urlpatterns = [
    path('', views.events, name='list'),
    path('<int:event_id>/', views.event_detail, name='detail'),
]
```

В главном URLconf приложение подключено через `path('events/', include('events_web.urls'))`. Шаблоны используют `events:list` и `events:detail`. Если переименовать `app_name` в `calendar`, нужно соответственно обновить `{% url 'events:list' %}` и `{% url 'events:detail' ... %}` во всех шаблонах. Иначе возникает `NoReverseMatch` при построении ссылок. Пространство имён помогает не путать маршрут `detail` у разных приложений.

## 15. Конвертер параметра маршрута `<int:...>`

**Где показать:** `events_web/urls.py`:

```python
path('<int:event_id>/', views.event_detail, name='detail')
```

**Проверка:** `/events/1/` соответствует маршруту, а `/events/abc/` **не соответствует** шаблону `int` и вызывает 404 на этапе сопоставления URL. Представление `event_detail()` для текста `abc` не вызывается. Внутрь view передаётся `int` (в JSON ID записаны строками, функция `find_event_by_id()` сама сравнивает через `str(event_id)`).

## 16. Обработка отсутствующих объектов

**Где показать:** `events_web/views.py`, `event_detail()`:

```python
event = find_event_by_id(load_events(), event_id)
if event is None:
    raise Http404('Событие не найдено')
```

Для адреса `/events/999/` маршрут подходит, но событие с таким ID в `data/events.json` отсутствует. Функция поиска возвращает `None`, после чего view вызывает `Http404`. **Результат:** HTTP-статус 404, а не страница с неверными данными и не ошибка 500. Для приглашения такой же приём используется в `invitations_web/views.py`.

## 17. Ошибка маршрутизации и ошибка поиска объекта

**Где показать:** `events_web/urls.py`, `events_web/views.py`.

Сравнение двух случаев:

- `/wrong-address/`: подходящий `path()` в проекте не найден → 404 создаётся **URL-диспетчером** до запуска view.
- `/events/999/`: маршрут с `<int:event_id>` найден → запускается `event_detail()` → поиск в JSON возвращает `None` → view вызывает `Http404`.

**Результат для браузера в обоих случаях:** 404, но причина и место возникновения разные. При `DEBUG=True` отладочная страница Django помогает понять, какой путь проверялся.

## 18. Ошибка поиска шаблона и ошибка внутри шаблона

**Где показать:** `events_web/views.py`:

```python
return render(request, 'events_web/event_list.html', context)
```

**Эксперимент 1:** временно укажите `events_web/not_found.html`. Если файла нет, Django выдаст `TemplateDoesNotExist` (обычно ответ 500, подробности при `DEBUG=True`).

**Эксперимент 2:** верните путь, но в шаблоне напишите незакрытый `{% for %}`. Возникнет `TemplateSyntaxError`: файл найден, но его содержимое некорректно. Отличие: первая ошибка относится к поиску файла, вторая — к разбору синтаксиса. Верните корректный путь и теги.

## 19. Поиск и исправление синтаксической ошибки шаблона

**Где показать:** `events_web/templates/events_web/event_list.html`.

Нормальная конструкция:

```django
{% for event in events %}
  {% include 'events_web/includes/event_card.html' %}
{% empty %}
  <div>Событий нет</div>
{% endfor %}
```

**Эксперимент:** временно удалите `{% endfor %}`. Django не сможет закончить разбор блока цикла и при открытии `/events/` сообщит `TemplateSyntaxError`. Исправление — вернуть завершающий тег. Аналогично незакрытый `{% if %}` требует `{% endif %}`. IDE с подсветкой шаблонов облегчает поиск таких ошибок.

## 20. Подключение статических ресурсов

**Где показать:** `templates/base.html`:

```django
{% load static %}
<link rel="stylesheet" href="{% static 'homepage/css/style.css' %}">
<script src="{% static 'homepage/js/main.js' %}" defer></script>
<img src="{% static 'homepage/img/logo.png' %}" alt="Логотип">
```

Логотип фактически включён в `templates/includes/navigation.html`, не обязательно оставлять пример `img` в `base.html`. Файлы лежат в `homepage/static/homepage/`. **Демонстрация:** поменяйте только в шаблоне путь CSS на `homepage/css/missing.css`. В браузере `F12 → Network` будет запрос к отсутствующему ресурсу (обычно 404), а оформление исчезнет или изменится. Верните верный путь.

## 21. Изменение CSS-стилей

**Где показать:** `events_web/templates/events_web/includes/event_card.html` и `homepage/static/homepage/css/style.css`.

Карточка содержит `<article class="entry-card event-card">`. CSS определяет, в частности:

```css
.entry-card {
  background: #fff;
  border: 1px solid var(--line);
  border-radius: 20px;
}
```

**Демонстрация:** добавьте **временно** в конец CSS правило `.event-card { border: 3px solid red; }`, затем обновите `/events/` (при необходимости `Ctrl+F5`). Рамка карточек событий станет красной. Селектор `.event-card` выбирает HTML-элементы с таким `class`. После защиты удалите тестовое правило.

## 22. Диагностика JavaScript

**Где показать:** `templates/base.html`, `templates/includes/navigation.html`, `homepage/static/homepage/js/main.js`.

В `base.html` подключён `main.js` через `{% static %}` и `defer`. В навигации кнопка `id="nav-toggle"` управляет меню `id="site-nav"`. JS использует `getElementById()`, обработчик `click`, `aria-expanded` и класс `is-open`.

**Демонстрация:** сузьте браузер до мобильной ширины и нажмите «☰» — меню раскроется. Если реакция пропала: в `F12 → Network` проверьте загрузку `main.js` (404 означает неверный путь); если файл загрузился, в `Console` ищите JS-ошибку, проверяйте совпадение идентификаторов элементов и работу обработчика клика. Эти проблемы диагностируются по-разному.

## 23. Организация шаблонов по приложениям

**Где показать:** дерево папок проекта и view-функции:

```text
templates/base.html
templates/includes/navigation.html
events_web/templates/events_web/event_list.html
events_web/templates/events_web/event_detail.html
invitations_web/templates/invitations_web/invitation_list.html
invitations_web/templates/invitations_web/invitation_detail.html
homepage/templates/homepage/index.html
```

В `events_web/views.py` используется `render(request, 'events_web/event_list.html', context)`. В `inviteweb/settings.py` указан `APP_DIRS=True`, а `DIRS` включает общую `templates/`. Раздельные префиксы `events_web/`, `invitations_web/` защищают от коллизий: файлы с одинаковым коротким именем в разных приложениях не мешают друг другу.

## 24. Согласованность представления и шаблона

**Где показать:** `invitations_web/views.py` (функция `invitation_detail`) и `invitations_web/templates/invitations_web/invitation_detail.html`.

View передаёт контекст:

```python
return render(request, 'invitations_web/invitation_detail.html', {
    'page_title': f'Приглашение №{invitation.id}',
    'invitation': invitation,
    'event_date': date.fromisoformat(invitation.event.date),
})
```

Шаблон показывает `{{ invitation.guest_name }}`, `{{ invitation.event.name }}` и `{{ event_date|date:'d.m.Y' }}`. **Эксперимент:** переименуйте ключ `'invitation'` в `'invite'`, но шаблон не меняйте. Поля потеряют значения. Исправление — вернуть ключ или изменить все обращения на `invite.*`. Совпадение имён — контракт между view и шаблоном.

## 25. Полный путь HTTP-запроса

**Где показать:** `inviteweb/urls.py`, `events_web/urls.py`, `events_web/views.py`, `events_web/templates/events_web/event_detail.html`.

**Путь `/events/1/`:**

1. Браузер отправляет GET `/events/1/`.
2. Главный `inviteweb/urls.py` сопоставляет префикс `events/` и передаёт остаток `1/` в `events_web.urls`.
3. `path('<int:event_id>/', views.event_detail, name='detail')` превращает `1` в целое число `event_id=1`.
4. В `event_detail()` вызывается `load_events()` из `storage.py`, читающий `data/events.json`. Поиск `find_event_by_id(..., 1)` возвращает объект `Event` (строковый ID из JSON сравнивается со `str(1)`).
5. View формирует контекст `event`, `event_date`, `is_upcoming`, `page_title` и вызывает `render(request, 'events_web/event_detail.html', context)`.
6. `event_detail.html` наследует `base.html`, выводит `{{ event.name }}`, дату, организатора и ссылку назад; Django формирует HTML-ответ HTTP 200.
7. Если `/events/999/` не соответствует существующему объекту, view вызывает `Http404`, и ответ становится 404. Если `/events/abc/`, до view дело вообще не доходит: числовой конвертер не совпадает.

**Вывод для защиты:** URLconf отвечает за маршрутизацию; view — за получение данных и подготовку контекста; Django-шаблон — за HTML; статические файлы — за оформление и интерактивность.

---

## Карта файлов: что открывать на защите

| Вопросы | Файлы |
|---|---|
| 1, 2, 5 | `templates/base.html`, `homepage/templates/homepage/index.html` |
| 3, 4, 7, 9, 10, 12, 13, 19, 21 | `events_web/views.py`, `events_web/templates/events_web/event_list.html`, `events_web/templates/events_web/includes/event_card.html` |
| 6, 15, 16, 17, 18, 25 | `events_web/urls.py`, `events_web/views.py`, `events_web/templates/events_web/event_detail.html` |
| 8, 11, 24 | `invitations_web/views.py`, `invitations_web/templates/invitations_web/`, `data/invitations.json` |
| 14 | `events_web/urls.py`, `inviteweb/urls.py`, `templates/includes/navigation.html` |
| 20, 22 | `templates/base.html`, `templates/includes/navigation.html`, `homepage/static/homepage/` |
| 23 | `inviteweb/settings.py` и папки `templates/` во всех приложениях |

## Документация, с которой сверены ответы

- Язык шаблонов Django: https://docs.djangoproject.com/en/5.2/ref/templates/language/
- Встроенные теги и фильтры: https://docs.djangoproject.com/en/5.2/ref/templates/builtins/
- Маршрутизация: https://docs.djangoproject.com/en/5.2/topics/http/urls/
- Работа со статическими файлами: https://docs.djangoproject.com/en/5.2/howto/static-files/

**Важно:** в этих ответах временные опыты и ожидаемое поведение приведены как сценарии для демонстрации. Они не означают, что все 25 изменений одновременно применены к исходному проекту. На самой защите выполняйте один опыт за раз и отменяйте тестовые правки.
