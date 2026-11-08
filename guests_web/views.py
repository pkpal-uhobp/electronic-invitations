"""Guests and their related invitations via Django ORM."""
from django.shortcuts import get_object_or_404, render

from .models import Guest
from invitations_web.models import Invitation


def guests(request):
    result = Guest.objects.all().order_by('name', 'pk')
    return render(request, 'guests_web/guest_list.html', {
        'page_title': 'Гости', 'guests': result,
    })


def guest_detail(request, guest_id: int):
    guest = get_object_or_404(Guest, pk=guest_id)
    invitations = (Invitation.objects.filter(guest=guest)
                   .select_related('event', 'guest').order_by('pk'))
    return render(request, 'guests_web/guest_detail.html', {
        'page_title': guest.name, 'guest': guest, 'invitations': invitations,
    })
