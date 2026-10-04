"""View-функции раздела гостей."""

from html import escape

from django.http import HttpResponse

from guests import find_guest_by_id, sort_guests
from homepage.views import page
from models import Guest
from storage import load_events, load_guests, load_invitations


def guests(request):
    """Показать список гостей из data/guests.json."""
    guest_list = sort_guests(load_guests())
    invitations = load_invitations(load_events(), guest_list)
    items = ""

    for guest in guest_list:
        invitation_count = sum(
            1
            for invitation in invitations
            if isinstance(invitation.guest, Guest)
            and invitation.guest.id == guest.id
        )
        items += f"""
        <a href="/guests/{guest.id}/"
           class="list-group-item list-group-item-action">
          <div class="d-flex w-100 justify-content-between gap-3">
            <div>
              <strong>{escape(guest.name)}</strong>
              <div class="small text-muted">{escape(guest.email)}</div>
            </div>
            <span class="badge text-bg-primary align-self-center">
              приглашений: {invitation_count}
            </span>
          </div>
        </a>
        """

    if not items:
        items = (
            '<div class="alert alert-info">'
            "Гости пока отсутствуют в data/guests.json."
            "</div>"
        )

    content = f"""
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h1>Гости</h1>
      <span class="badge text-bg-primary">{len(guest_list)}</span>
    </div>
    <p class="text-muted">
      Гость — отдельная сущность, на которую ссылается приглашение.
    </p>
    <div class="list-group app-card">{items}</div>
    """
    return HttpResponse(page("Гости", content))


def guest_detail(request, guest_id: int):
    """Показать гостя и его приглашения."""
    guest_list = load_guests()
    guest = find_guest_by_id(guest_list, guest_id)
    if guest is None:
        content = """
        <div class="alert alert-danger">
          <h1 class="h3">Гость не найден</h1>
          <a href="/guests/" class="btn btn-outline-danger">
            ← к списку гостей
          </a>
        </div>
        """
        return HttpResponse(page("Гость не найден", content), status=404)

    invitations = load_invitations(load_events(), guest_list)
    guest_invitations = [
        invitation
        for invitation in invitations
        if isinstance(invitation.guest, Guest)
        and invitation.guest.id == guest.id
    ]
    invitation_items = "".join(
        f'<li class="list-group-item"><a href="/invitations/{item.id}/">'
        f'Приглашение №{item.id}</a> — '
        f'<a href="/events/{item.event.id}/">{escape(item.event.name)}</a>'
        f' ({item.response})</li>'
        for item in guest_invitations
    )
    if not invitation_items:
        invitation_items = (
            '<li class="list-group-item text-muted">Приглашений нет</li>'
        )

    content = f"""
    <div class="card app-card mb-4">
      <div class="card-body">
        <h1 class="card-title h2">{escape(guest.name)}</h1>
        <p><strong>ID:</strong> {guest.id}</p>
        <p><strong>Email:</strong> {escape(guest.email)}</p>
      </div>
    </div>
    <h2 class="h4">Приглашения гостя</h2>
    <ul class="list-group app-card mb-3">{invitation_items}</ul>
    <a href="/guests/" class="btn btn-outline-secondary">
      ← к списку гостей
    </a>
    """
    return HttpResponse(page(guest.name, content))
