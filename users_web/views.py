"""View-функции раздела пользователей-организаторов."""

from html import escape

from django.http import HttpResponse

from homepage.views import page
from storage import load_events, load_users
from users import find_user_by_id, sort_users


def users(request):
    """Показать список пользователей из data/users.json."""
    user_list = sort_users(load_users())
    events = load_events(user_list)
    items = ""

    for user in user_list:
        event_count = sum(
            1 for event in events if event.user and event.user.id == user.id
        )
        items += f"""
        <a href="/users/{user.id}/"
           class="list-group-item list-group-item-action">
          <div class="d-flex w-100 justify-content-between gap-3">
            <div>
              <strong>{escape(user.name)}</strong>
              <div class="small text-muted">{escape(user.email)}</div>
            </div>
            <span class="badge text-bg-primary align-self-center">
              событий: {event_count}
            </span>
          </div>
        </a>
        """

    if not items:
        items = (
            '<div class="alert alert-info">'
            "Пользователи пока отсутствуют в data/users.json."
            "</div>"
        )

    content = f"""
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h1>Пользователи</h1>
      <span class="badge text-bg-primary">{len(user_list)}</span>
    </div>
    <p class="text-muted">Пользователь — организатор и владелец событий.</p>
    <div class="list-group app-card">{items}</div>
    """
    return HttpResponse(page("Пользователи", content))


def user_detail(request, user_id: int):
    """Показать пользователя и созданные им события."""
    user_list = load_users()
    user = find_user_by_id(user_list, user_id)
    if user is None:
        content = """
        <div class="alert alert-danger">
          <h1 class="h3">Пользователь не найден</h1>
          <a href="/users/" class="btn btn-outline-danger">
            ← к списку пользователей
          </a>
        </div>
        """
        return HttpResponse(page("Пользователь не найден", content), status=404)

    events = [
        event
        for event in load_events(user_list)
        if event.user and event.user.id == user.id
    ]
    event_items = "".join(
        f'<li class="list-group-item"><a href="/events/{event.id}/">'
        f'{escape(event.name)}</a> — {event.date}</li>'
        for event in events
    )
    if not event_items:
        event_items = '<li class="list-group-item text-muted">Событий нет</li>'

    content = f"""
    <div class="card app-card mb-4">
      <div class="card-body">
        <h1 class="card-title h2">{escape(user.name)}</h1>
        <p><strong>ID:</strong> {user.id}</p>
        <p><strong>Email:</strong> {escape(user.email)}</p>
      </div>
    </div>
    <h2 class="h4">События пользователя</h2>
    <ul class="list-group app-card mb-3">{event_items}</ul>
    <a href="/users/" class="btn btn-outline-secondary">
      ← к списку пользователей
    </a>
    """
    return HttpResponse(page(user.name, content))
