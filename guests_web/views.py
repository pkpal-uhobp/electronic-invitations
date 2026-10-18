"""Гости и связанные с ними приглашения (JSON)."""
from django.http import Http404
from django.shortcuts import render
from guests import find_guest_by_id, sort_guests
from models import Guest
from storage import load_events, load_guests, load_invitations


def guests(request):
    guest_list = sort_guests(load_guests())
    invites = load_invitations(load_events(), guest_list)
    counts = {g.id: sum(isinstance(i.guest, Guest) and i.guest.id == g.id for i in invites)
              for g in guest_list}
    return render(request, 'guests_web/guest_list.html', {
        'page_title': 'Гости', 'guests': guest_list, 'counts': counts,
    })


def guest_detail(request, guest_id: int):
    guest_list = load_guests()
    guest = find_guest_by_id(guest_list, guest_id)
    if guest is None:
        raise Http404('Гость не найден')
    invites = load_invitations(load_events(), guest_list)
    guest_invites = [i for i in invites if isinstance(i.guest, Guest) and i.guest.id == guest.id]
    return render(request, 'guests_web/guest_detail.html', {
        'page_title': guest.name, 'guest': guest, 'invitations': guest_invites,
    })
