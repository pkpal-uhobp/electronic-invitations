"""PR10 regression tests: admin, manager, slugs, generated fields and SQL."""
from datetime import date
import re

import pytest
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError, connection, transaction
from django.db.models import F, Q
from django.test import Client
from django.test.utils import CaptureQueriesContext
from django.urls import reverse

from events_web.admin import EventAdmin, EventInvitationInline
from events_web.models import Event
from guests_web.admin import GuestAdmin
from guests_web.models import Guest
from invitations_web.admin import InvitationAdmin
from invitations_web.models import Invitation
from users_web.admin import UserAdmin
from users_web.models import User

pytestmark = pytest.mark.django_db


@pytest.fixture
def sample():
    organizer = User.objects.create(name='Алексей', email='a@example.com')
    guest = Guest.objects.create(name='Анна', email='anna@example.com')
    event = Event.objects.create(
        name='День рождения', date=date(2027, 1, 15), user=organizer)
    invite = Invitation.objects.create(event=event, guest=guest, guest_name='Анна')
    return organizer, guest, event, invite


def test_four_models_registered_once_with_configured_admins():
    assert isinstance(admin.site._registry[Event], EventAdmin)
    assert isinstance(admin.site._registry[User], UserAdmin)
    assert isinstance(admin.site._registry[Guest], GuestAdmin)
    assert isinstance(admin.site._registry[Invitation], InvitationAdmin)
    assert EventInvitationInline in admin.site._registry[Event].inlines
    assert 'status' in admin.site._registry[Invitation].list_filter
    assert 'event__name' in admin.site._registry[Invitation].search_fields
    assert Event._meta.verbose_name == 'Событие'
    assert Event._meta.get_field('date').verbose_name == 'Дата проведения'


def test_admin_superuser_login_and_related_changelists(sample):
    user = get_user_model().objects.create_superuser(
        username='pr10_admin', email='root@example.com', password='testing1234!')
    client = Client()
    assert client.get('/admin/').status_code == 302
    client.force_login(user)
    for model in (User, Guest, Event, Invitation):
        path = reverse(f'admin:{model._meta.app_label}_{model._meta.model_name}_changelist')
        response = client.get(path)
        assert response.status_code == 200
    event_change = reverse('admin:events_web_event_change', args=[sample[2].pk])
    assert client.get(event_change).status_code == 200


def test_slug_transliteration_and_old_url_compatibility(sample):
    event = sample[2]
    assert re.fullmatch(r'[a-z0-9-]+', event.slug)
    assert event.slug.startswith('den-rozhdeniia-') or event.slug.startswith('den-rozhdeniya-')
    assert event.slug.endswith(f'-{event.pk}')
    assert event.get_absolute_url() == reverse('events:detail_slug', args=[event.slug])
    client = Client()
    assert client.get(event.get_absolute_url()).status_code == 200
    assert client.get(reverse('events:detail', args=[event.pk])).status_code == 200
    assert client.get('/events/not-there-999999/').status_code == 404


def test_slugs_unique_and_stable_on_rename(sample):
    event = sample[2]
    other = Event.objects.create(name=event.name, date=event.date)
    assert other.slug != event.slug
    original = event.slug
    event.name = 'Новое название'
    event.save(update_fields=['name'])
    event.refresh_from_db()
    assert event.slug == original
    assert other.slug.endswith(f'-{other.pk}')


def test_slug_fallback_and_max_length():
    event = Event.objects.create(name='!!!', date=date(2027, 1, 1))
    assert event.slug == f'event-{event.pk}'
    long_name = Event.objects.create(name='А' * 200, date=date(2027, 1, 1))
    assert len(long_name.slug) <= 180


def test_generated_field_computed_by_sqlite_and_refresh(sample):
    event = sample[2]
    event.refresh_from_db()
    assert event.name_length == len(event.name)
    assert Event._meta.get_field('name_length').generated
    event.name = 'Форум'
    event.save(update_fields=['name'])
    event.refresh_from_db()
    assert event.name_length == 5


def test_textchoices_and_queryset_manager(sample):
    organizer, guest, event, invite = sample
    cancelled = Invitation.objects.create(
        event=event, guest_name='Иван', status=Invitation.Status.CANCELLED)
    completed = Invitation.objects.create(
        event=event, guest_name='Мария', status=Invitation.Status.COMPLETED)
    assert list(Invitation.objects.active()) == [invite]
    assert list(Invitation.objects.cancelled()) == [cancelled]
    assert list(Invitation.objects.completed()) == [completed]
    assert Invitation.objects.for_event(event).count() == 3
    assert completed.get_status_display() == 'Завершено'


def test_guest_availability_only_active_blocks(sample):
    _, guest, event, active = sample
    other = Guest.objects.create(name='Иван', email='ivan@example.com')
    Invitation.objects.create(event=event, guest=other, guest_name='Иван',
                              status=Invitation.Status.COMPLETED)
    client = Client()
    response = client.get(reverse('events:available'), {'event_id': event.pk})
    assert list(response.context['available'].values_list('pk', flat=True)) == [other.pk]
    active.complete()
    response = client.get(reverse('events:available'), {'event_id': event.pk})
    assert set(response.context['available'].values_list('pk', flat=True)) == {
        other.pk, guest.pk}


def test_duplicate_active_guest_rejected_by_model_and_database(sample):
    _, guest, event, _ = sample
    duplicate = Invitation(event=event, guest=guest, guest_name='Анна')
    with pytest.raises(ValidationError):
        duplicate.full_clean()
    with pytest.raises(IntegrityError), transaction.atomic():
        Invitation.objects.create(event=event, guest=guest, guest_name='Анна')
    # Cancelled invitations may coexist with an active invitation.
    Invitation.objects.create(event=event, guest=guest, guest_name='Анна',
                              status=Invitation.Status.CANCELLED)


def test_guest_name_duplicate_without_foreign_key_rejected(sample):
    _, _, event, _ = sample
    Invitation.objects.create(event=event, guest_name='Свободный гость')
    for name in ('свободный гость', 'СВОБОДНЫЙ ГОСТЬ',
                 '  СвоБоДныЙ Гость  '):
        duplicate = Invitation(event=event, guest_name=name)
        with pytest.raises(ValidationError):
            duplicate.full_clean()
    # Another event is allowed, as is a cancelled invitation on the same event.
    other_event = Event.objects.create(name='Другое событие', date=event.date)
    Invitation(event=other_event, guest_name='свободный гость').full_clean()
    Invitation(event=event, guest_name='свободный гость',
               status=Invitation.Status.CANCELLED).full_clean()


def test_context_processor_and_site_navigation(sample):
    response = Client().get(reverse('events:list'))
    assert response.context['site_name'] == 'Электронные приглашения'
    assert response.context['events_count'] == 1
    assert 'События (1)' in response.content.decode('utf-8')
    assert Client().get(reverse('invitations:list')).context['events_count'] == 1


def test_status_filter_and_statistics_completed(sample):
    _, _, event, invite = sample
    invite.complete()
    response = Client().get(reverse('invitations:list'), {'status': 'completed'})
    assert response.context['page_obj'].paginator.count == 1
    stats = Client().get(reverse('invitations:statistics'))
    assert stats.context['completed_count'] == 1
    assert stats.context['totals']['active'] == 0
    assert stats.context['totals']['total'] == 1
    assert stats.context['by_event'].get(pk=event.pk).completed_count == 1


def test_f_values_linked_queries_one_statement(sample):
    query = Invitation.objects.annotate(
        event_name=F('event__name'), organizer_name=F('event__user__name'),
    ).values('guest_name', 'event_name', 'organizer_name')
    with CaptureQueriesContext(connection) as captured:
        rows = list(query)
    assert len(captured) == 1
    assert rows[0]['event_name'] == sample[2].name
    assert rows[0]['organizer_name'] == sample[0].name


def test_q_filter_exclude_and_admin_related_without_nplusone(sample):
    organizer, guest, event, invitation = sample
    assert Invitation.objects.filter(Q(event__name__icontains='рожден') |
                                     Q(guest__email='nobody@example.com')).count() == 1
    assert Invitation.objects.exclude(status=Invitation.Status.CANCELLED).count() == 1
    with CaptureQueriesContext(connection) as captured:
        invites = list(Invitation.objects.select_related('event', 'guest', 'event__user'))
        names = [(i.event.name, i.guest.name, i.event.user.name) for i in invites]
    assert len(captured) == 1
    assert names == [(event.name, guest.name, organizer.name)]


def test_new_urls_use_slug_in_site_links(sample):
    response = Client().get(reverse('events:list'))
    assert sample[2].get_absolute_url() in response.content.decode('utf-8')
    detail = Client().get(reverse('invitations:detail', args=[sample[3].pk]))
    assert sample[2].get_absolute_url() in detail.content.decode('utf-8')
