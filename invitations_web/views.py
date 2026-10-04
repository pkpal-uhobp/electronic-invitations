"""View-функции раздела электронных приглашений."""

from html import escape

from django.http import HttpResponse

from homepage.views import page
from invitations import find_invitation_by_id, sort_invitations
from models import Guest
from storage import load_events, load_guests, load_invitations


def _status_badge(status: str) -> tuple[str, str]:
    """Вернуть текст и Bootstrap-класс статуса приглашения."""
    if status == "cancelled":
        return "отменено", "text-bg-secondary"
    return "активно", "text-bg-success"


def _response_badge(response: str) -> tuple[str, str]:
    """Вернуть текст и Bootstrap-класс ответа гостя."""
    if response == "да":
        return "придёт", "text-bg-success"
    if response == "нет":
        return "не придёт", "text-bg-danger"
    return "не определено", "text-bg-warning"


def _guest_html(invitation) -> str:
    """Сформировать ссылку на гостя, если сущность Guest восстановлена."""
    name = escape(invitation.guest_name)
    if isinstance(invitation.guest, Guest):
        return f'<a href="/guests/{invitation.guest.id}/">{name}</a>'
    return name


def invitations(request):
    """Показать список приглашений из data/invitations.json."""
    events = load_events()
    guests = load_guests()
    invitation_list = sort_invitations(load_invitations(events, guests))
    items = ""

    for invitation in invitation_list:
        status_text, status_badge = _status_badge(invitation.status)
        guest = _guest_html(invitation)
        event_name = escape(invitation.event.name)
        items += f"""
        <div class="list-group-item">
          <div class="d-flex w-100 justify-content-between gap-3">
            <div>
              <strong>{guest}</strong>
              <div class="small text-muted">
                <a href="/events/{invitation.event.id}/">{event_name}</a>
              </div>
              <a class="small" href="/invitations/{invitation.id}/">
                открыть приглашение №{invitation.id}
              </a>
            </div>
            <span class="badge {status_badge} align-self-center">
              {status_text}
            </span>
          </div>
        </div>
        """

    if not items:
        items = (
            '<div class="alert alert-info">'
            "Приглашения пока отсутствуют в data/invitations.json."
            "</div>"
        )

    content = f"""
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h1>Приглашения</h1>
      <span class="badge text-bg-primary">{len(invitation_list)}</span>
    </div>
    <div class="list-group app-card">{items}</div>
    """
    return HttpResponse(page("Приглашения", content))


def invitation_detail(request, invitation_id: int):
    """Показать карточку приглашения или вернуть HTTP 404."""
    events = load_events()
    guests = load_guests()
    invitation_list = load_invitations(events, guests)
    invitation = find_invitation_by_id(invitation_list, invitation_id)

    if invitation is None:
        content = """
        <div class="alert alert-danger">
          <h1 class="h3">Приглашение не найдено</h1>
          <p class="mb-3">Приглашения с таким идентификатором нет.</p>
          <a href="/invitations/" class="btn btn-outline-danger">
            ← к списку приглашений
          </a>
        </div>
        """
        return HttpResponse(
            page("Приглашение не найдено", content),
            status=404,
        )

    status_text, status_badge = _status_badge(invitation.status)
    response_text, response_badge = _response_badge(invitation.response)
    guest = _guest_html(invitation)
    event_name = escape(invitation.event.name)
    guest_email = ""
    if isinstance(invitation.guest, Guest):
        guest_email = (
            f'<p class="card-text"><strong>Email гостя:</strong> '
            f'{escape(invitation.guest.email)}</p>'
        )

    content = f"""
    <div class="card app-card">
      <div class="card-body">
        <h1 class="card-title h2">Приглашение №{invitation.id}</h1>
        <p class="card-text"><strong>Гость:</strong> {guest}</p>
        {guest_email}
        <p class="card-text">
          <strong>Событие:</strong>
          <a href="/events/{invitation.event.id}/">{event_name}</a>
        </p>
        <p class="card-text">
          <strong>Дата:</strong> {invitation.event.date}
        </p>
        <p class="card-text">
          <strong>Статус:</strong>
          <span class="badge {status_badge}">{status_text}</span>
        </p>
        <p class="card-text">
          <strong>Ответ гостя:</strong>
          <span class="badge {response_badge}">{response_text}</span>
        </p>
        <a href="/invitations/" class="btn btn-outline-secondary">
          ← к списку приглашений
        </a>
      </div>
    </div>
    """
    return HttpResponse(
        page(f"Приглашение №{invitation.id}", content),
        status=200,
    )
