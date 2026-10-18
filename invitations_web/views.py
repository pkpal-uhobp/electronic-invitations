"""Приглашения: JSON → объекты → render()."""
from datetime import date
from django.http import Http404
from django.shortcuts import render
from invitations import find_invitation_by_id, sort_invitations
from storage import load_events, load_guests, load_invitations


def invitations(request):
    invitations_list = sort_invitations(load_invitations(load_events(), load_guests()))
    return render(request, 'invitations_web/invitation_list.html', {
        'page_title': 'Приглашения', 'invitations': invitations_list,
    })


def invitation_detail(request, invitation_id: int):
    invitation = find_invitation_by_id(
        load_invitations(load_events(), load_guests()), invitation_id
    )
    if invitation is None:
        raise Http404('Приглашение не найдено')
    return render(request, 'invitations_web/invitation_detail.html', {
        'page_title': f'Приглашение №{invitation.id}', 'invitation': invitation,
        'event_date': date.fromisoformat(invitation.event.date),
    })
