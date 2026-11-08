"""PR9 integration tests: models, migrations, CRUD, relations, queries, views."""
from datetime import date
from pathlib import Path
import sqlite3

import pytest
from django.core.management import call_command
from django.db.models import Count, Q
from django.test import Client
from django.urls import reverse

from events_web.models import Event
from guests_web.models import Guest
from invitations_web.models import Invitation
from users_web.models import User

pytestmark = pytest.mark.django_db


@pytest.fixture
def dataset():
    alice = User.objects.create(name='Алексей', email='alexey@example.com')
    yana = User.objects.create(name='Яна', email='yana@example.com')
    anna = Guest.objects.create(name='Анна', email='anna@example.com')
    ivan = Guest.objects.create(name='Иван', email='ivan@example.com')
    maria = Guest.objects.create(name='Мария', email='maria@example.com')
    e1 = Event.objects.create(name='День рождения', date=date(2026, 12, 25), user=alice)
    e2 = Event.objects.create(name='Новый год', date=date(2026, 12, 31), user=yana)
    i1 = Invitation.objects.create(event=e1, guest=anna, guest_name='Анна', response='да')
    i2 = Invitation.objects.create(event=e1, guest=ivan, guest_name='Иван', response='нет',
                                   status='cancelled')
    i3 = Invitation.objects.create(event=e2, guest=anna, guest_name='Анна')
    return locals()


def test_models_crud_and_relations(dataset):
    d = dataset
    assert d['alice'].events.get(pk=d['e1'].pk) == d['e1']
    assert d['anna'].invitations.count() == 2
    assert d['e1'].invitations.count() == 2
    assert Event.objects.get(pk=d['e1'].pk).name == 'День рождения'
    assert Invitation.objects.filter(event__user__name='Алексей').count() == 2
    assert Invitation.objects.filter(status='active', event=d['e1']).count() == 1
    assert Invitation.objects.exclude(status='cancelled').count() == 2
    assert Event.objects.filter(Q(name__icontains='год') | Q(user__name='Яна')).count() == 1
    assert list(Event.objects.order_by('-date').values_list('pk', flat=True)) == [
        d['e2'].pk, d['e1'].pk]
    assert Event.objects.values('name').count() == 2
    assert Event.objects.annotate(n=Count('invitations')).get(pk=d['e1'].pk).n == 2
    assert Invitation.objects.aggregate(n=Count('pk'))['n'] == 3
    assert Invitation.objects.select_related('event', 'guest').first().event is not None
    d['i1'].set_response('нет')
    assert Invitation.objects.get(pk=d['i1'].pk).response == 'нет'
    d['i1'].cancel()
    assert Invitation.objects.get(pk=d['i1'].pk).status == 'cancelled'
    d['i1'].delete()
    assert not Invitation.objects.filter(pk=d['i1'].pk).exists()


def test_on_delete_set_null_and_cascade(dataset):
    d = dataset
    d['alice'].delete()
    d['anna'].delete()
    d['e1'].refresh_from_db()
    d['i1'].refresh_from_db()
    assert d['e1'].user_id is None
    assert d['i1'].guest_id is None
    d['e1'].delete()
    assert not Invitation.objects.filter(pk=d['i1'].pk).exists()
    assert Invitation.objects.filter(pk=d['i3'].pk).exists()


def test_home_and_detail_pages(dataset):
    client = Client()
    for name in ('homepage:index', 'events:list', 'invitations:list', 'users:list',
                 'guests:list', 'events:search', 'events:available',
                 'invitations:statistics'):
        assert client.get(reverse(name)).status_code == 200
    for name, pk in [('events:detail', dataset['e1'].pk),
                     ('invitations:detail', dataset['i1'].pk),
                     ('users:detail', dataset['alice'].pk),
                     ('guests:detail', dataset['anna'].pk)]:
        assert client.get(reverse(name, args=[pk])).status_code == 200
        assert client.get(reverse(name, args=[99999])).status_code == 404


def test_search_and_available_guests(dataset):
    client = Client()
    response = client.get(reverse('events:search'), {'date': '2026-12-25'})
    assert response.status_code == 200
    assert b'html' in response.content
    assert len(response.context['events']) == 1
    bad = client.get(reverse('events:search'), {'date': 'not-a-date'})
    assert bad.context['error']
    selected = client.get(reverse('events:available'), {'event_id': dataset['e1'].pk})
    assert list(selected.context['available'].values_list('name', flat=True)) == [
        'Иван', 'Мария']  # cancelled invitation does not block availability
    selected = client.get(reverse('events:available'), {'event_id': 'broken'})
    assert selected.context['error']


def test_invitations_filters_and_safe_sorting(dataset):
    client = Client()
    url = reverse('invitations:list')
    a = client.get(url, {'status': 'active', 'event_id': dataset['e1'].pk})
    assert a.context['page_obj'].paginator.count == 1
    a = client.get(url, {'q': 'anna@example.com'})
    assert a.context['page_obj'].paginator.count == 2
    a = client.get(url, {'hide_cancelled': 1})
    assert a.context['page_obj'].paginator.count == 2
    a = client.get(url, {'sort': 'bogus__field'})
    assert a.status_code == 200
    assert a.context['selected_sort'] == 'id'
    a = client.get(url, {'event_id': 'broken'})
    assert a.status_code == 200
    assert a.context['page_obj'].paginator.count == 0
    assert a.context['errors']
    a = client.get(url, {'status': 'invalid'})
    assert a.context['selected_status'] == ''


def test_pagination_keeps_query_parameters(dataset):
    event = dataset['e1']
    for n in range(9):
        Invitation.objects.create(event=event, guest_name=f'Дополнительный {n}',
                                  status='active')
    client = Client()
    response = client.get(reverse('invitations:list'), {
        'status': 'active', 'sort': 'guest', 'page': 2,
    })
    assert response.context['page_obj'].number == 2
    assert response.context['page_obj'].paginator.count == 11
    assert 'status=active' in response.content.decode()
    assert 'sort=guest' in response.content.decode()
    bad = client.get(reverse('invitations:list'), {'page': 'abc'})
    assert bad.context['page_obj'].number == 1
    far = client.get(reverse('invitations:list'), {'page': 999})
    assert far.context['page_obj'].number == far.context['page_obj'].paginator.num_pages


def test_aggregate_stats_including_objects_without_relations(dataset):
    Guest.objects.create(name='Без приглашений', email='empty@example.com')
    User.objects.create(name='Без событий', email='u@example.com')
    Event.objects.create(name='Без приглашений', date=date(2027, 1, 1))
    client = Client()
    response = client.get(reverse('invitations:statistics'))
    assert response.context['totals'] == {
        'total': 3, 'active': 2, 'cancelled': 1, 'yes_count': 1}
    by_event = {obj.name: obj.invitation_count for obj in response.context['by_event']}
    assert by_event['Без приглашений'] == 0
    by_organizer = {obj.name: obj.event_count for obj in response.context['by_organizer']}
    assert by_organizer['Без событий'] == 0
    assert len(response.context['popular']) == 1


def test_import_pr7_idempotent_and_preserves_foreign_keys(tmp_path):
    from db.import_json import import_json
    source = tmp_path / 'old.sqlite'
    data_dir = Path(__file__).resolve().parent.parent / 'data'
    import_json(data_dir=data_dir, db_path=source)
    call_command('import_pr7', '--source', str(source))
    call_command('import_pr7', '--source', str(source))
    assert User.objects.count() == 2
    assert Guest.objects.count() == 3
    assert Event.objects.count() == 2
    assert Invitation.objects.count() == 3
    assert Invitation.objects.get(pk=1).event_id == 1
    assert Invitation.objects.get(pk=1).guest_id == 1
    assert Event.objects.get(pk=1).date == date(2026, 10, 15)
    with sqlite3.connect(source) as connection:
        assert connection.execute('SELECT COUNT(*) FROM invitations').fetchone()[0] == 3


def test_null_foreign_keys_after_import(tmp_path):
    from db.import_json import import_json
    source = tmp_path / 'old.sqlite'
    import_json(Path(__file__).resolve().parent.parent / 'data', source)
    with sqlite3.connect(source) as conn:
        conn.execute('UPDATE events SET user_id=NULL WHERE id=1')
        conn.execute('UPDATE invitations SET guest_id=NULL WHERE id=1')
        conn.commit()
    call_command('import_pr7', '--source', str(source))
    assert Event.objects.get(pk=1).user_id is None
    assert Invitation.objects.get(pk=1).guest_id is None


def test_empty_database_is_safe():
    client = Client()
    for route in ('homepage:index', 'events:list', 'invitations:list',
                  'invitations:statistics', 'guests:list', 'users:list'):
        assert client.get(reverse(route)).status_code == 200
