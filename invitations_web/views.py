"""PR9: ORM search, filtering, safe ordering, relations, aggregates and pagination."""
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, render

from events_web.models import Event
from users_web.models import User
from .models import Invitation

SORTS = {
    'id': 'pk', 'date': 'event__date', 'date_desc': '-event__date',
    'guest': 'guest_name', 'event': 'event__name', 'status': 'status',
}


def invitations(request):
    status = request.GET.get('status', '').strip()
    if status not in (Invitation.STATUS_ACTIVE, Invitation.STATUS_CANCELLED):
        status = ''
    query = request.GET.get('q', '').strip()[:100]
    raw_event_id = request.GET.get('event_id', '').strip()
    sort = request.GET.get('sort', 'id')
    errors = []
    qs = Invitation.objects.select_related('event', 'guest', 'event__user')
    if status:
        qs = qs.filter(status=status)
    if request.GET.get('hide_cancelled') == '1':
        qs = qs.exclude(status=Invitation.STATUS_CANCELLED)
    if query:
        qs = qs.filter(Q(guest_name__icontains=query) | Q(event__name__icontains=query)
                       | Q(guest__email__icontains=query))
    if raw_event_id:
        if raw_event_id.isdecimal() and int(raw_event_id) > 0:
            qs = qs.filter(event_id=int(raw_event_id))
        else:
            errors.append('Некорректный идентификатор события.')
            qs = qs.none()
    if sort not in SORTS:
        sort = 'id'
    qs = qs.order_by(SORTS[sort], 'pk')
    page_obj = Paginator(qs, 5).get_page(request.GET.get('page', '1'))
    return render(request, 'invitations_web/invitation_list.html', {
        'page_title': 'Приглашения', 'invitations': page_obj.object_list,
        'page_obj': page_obj, 'selected_status': status,
        'query': query, 'selected_event': raw_event_id,
        'selected_sort': sort, 'events': Event.objects.all(), 'errors': errors,
        'hide_cancelled': request.GET.get('hide_cancelled') == '1',
    })


def invitation_detail(request, invitation_id: int):
    invite = get_object_or_404(
        Invitation.objects.select_related('event', 'guest', 'event__user'), pk=invitation_id)
    return render(request, 'invitations_web/invitation_detail.html', {
        'page_title': f'Приглашение №{invite.pk}',
        'invitation': invite, 'event_date': invite.event.date,
    })


def statistics(request):
    totals = Invitation.objects.aggregate(
        total=Count('pk'),
        active=Count('pk', filter=Q(status=Invitation.STATUS_ACTIVE)),
        cancelled=Count('pk', filter=Q(status=Invitation.STATUS_CANCELLED)),
        yes_count=Count('pk', filter=Q(response=Invitation.RESPONSE_YES)),
    )
    by_event = Event.objects.annotate(
        invitation_count=Count('invitations'),
        active_count=Count('invitations', filter=Q(invitations__status='active')),
    ).order_by('-invitation_count', 'pk')
    by_response = Invitation.objects.values('response').annotate(
        invitation_count=Count('pk')).order_by('-invitation_count', 'response')
    by_organizer = User.objects.annotate(event_count=Count('events')).order_by(
        '-event_count', 'pk')
    popular = Event.objects.annotate(invitation_count=Count('invitations')).filter(
        invitation_count__gte=2).order_by('-invitation_count', 'pk')
    return render(request, 'invitations_web/statistics.html', {
        'page_title': 'Статистика приглашений', 'totals': totals,
        'by_event': by_event, 'by_response': by_response,
        'by_organizer': by_organizer, 'popular': popular,
    })
