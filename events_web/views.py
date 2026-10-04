"""View-функции раздела событий."""

from datetime import date
from html import escape

from django.http import HttpResponse

from events import find_event_by_id, sort_events
from homepage.views import page
from storage import load_events


def _organizer_html(event) -> str:
    """Сформировать ссылку на пользователя-организатора."""
    if event.user is None:
        return '<span class="text-muted">не указан</span>'
    name = escape(event.user.name)
    return f'<a href="/users/{event.user.id}/">{name}</a>'


def events(request):
    """Показать список событий из data/events.json."""
    event_list = sort_events(load_events())
    items = ""
    for event in event_list:
        name = escape(event.name)
        organizer = _organizer_html(event)
        items += f"""
        <div class="list-group-item">
          <div class="d-flex w-100 justify-content-between">
            <strong>
              <a href="/events/{event.id}/">{name}</a>
            </strong>
            <span class="text-muted">{event.date}</span>
          </div>
          <small class="text-muted">ID: {event.id}</small>
          <div class="small">Организатор: {organizer}</div>
        </div>
        """

    if not items:
        items = (
            '<div class="alert alert-info">'
            "События пока отсутствуют в data/events.json."
            "</div>"
        )

    content = f"""
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h1>События</h1>
      <span class="badge text-bg-primary">{len(event_list)}</span>
    </div>
    <div class="list-group app-card">{items}</div>
    """
    return HttpResponse(page("События", content))


def event_detail(request, event_id: int):
    """Показать карточку события или вернуть HTTP 404."""
    event = find_event_by_id(load_events(), event_id)
    if event is None:
        content = """
        <div class="alert alert-danger">
          <h1 class="h3">Событие не найдено</h1>
          <p class="mb-3">События с таким идентификатором нет.</p>
          <a href="/events/" class="btn btn-outline-danger">
            ← к списку событий
          </a>
        </div>
        """
        return HttpResponse(
            page("Событие не найдено", content),
            status=404,
        )

    upcoming = event.date >= date.today().isoformat()
    status_text = "предстоит" if upcoming else "завершено"
    badge = "text-bg-success" if upcoming else "text-bg-secondary"
    name = escape(event.name)
    organizer = _organizer_html(event)
    content = f"""
    <div class="card app-card">
      <div class="card-body">
        <h1 class="card-title h2">{name}</h1>
        <p class="card-text"><strong>ID:</strong> {event.id}</p>
        <p class="card-text"><strong>Дата:</strong> {event.date}</p>
        <p class="card-text"><strong>Организатор:</strong> {organizer}</p>
        <p class="card-text">
          <strong>Статус:</strong>
          <span class="badge {badge}">{status_text}</span>
        </p>
        <a href="/events/" class="btn btn-outline-secondary">
          ← к списку событий
        </a>
      </div>
    </div>
    """
    return HttpResponse(page(name, content), status=200)
