"""ПР7: функциональные проверки SQLite, поисковых страниц и кастомных ошибок."""
import os
from pathlib import Path

import pytest

from db import database, queries
from db.import_json import import_json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inviteweb.settings')
django = pytest.importorskip('django')
django.setup()

from django.test import Client, RequestFactory, override_settings  # noqa: E402
from django.urls import reverse  # noqa: E402
from django.template.loader import get_template  # noqa: E402
from inviteweb import error_views  # noqa: E402


@pytest.fixture
def sqlite_db(tmp_path, monkeypatch):
    """Изолированная база, импортируемая из исходного JSON проекта."""
    path = tmp_path / 'invitations.sqlite'
    import_json(Path(__file__).resolve().parent.parent / 'data', path)
    monkeypatch.setattr(database, 'DB_PATH', path)
    return path


def test_schema_import_and_rows(sqlite_db):
    with database.get_connection() as conn:
        assert conn.execute('PRAGMA foreign_keys').fetchone()[0] == 1
        assert conn.execute('PRAGMA foreign_key_check').fetchall() == []
        result = conn.execute('SELECT name FROM events WHERE id = ?', (1,)).fetchone()
        assert result['name'] == 'День рождения'
        tables = {row['name'] for row in conn.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table'"
        )}
        assert {'events', 'users', 'guests', 'invitations'} <= tables


def test_import_is_idempotent(sqlite_db):
    data_dir = Path(__file__).resolve().parent.parent / 'data'
    for _ in range(2):
        assert import_json(data_dir, sqlite_db)['invitations'] == 3
    assert queries.one('total_counts')['invitations'] == 3


def test_19_named_queries_execute(sqlite_db):
    assert len(queries.catalog()) == 19
    args = {
        'event_by_id': (1,), 'invitation_by_id': (1,),
        'user_by_id': (1,), 'guest_by_id': (1,),
        'events_on_date': ('2026-10-15',), 'available_guests': (1,),
        'invitations_by_status': ('active',), 'invitations_for_guest': (1,),
        'events_for_user': (1,), 'popular_events': (2,),
    }
    for name in queries.catalog():
        queries.rows(name, args.get(name, ()))
    assert queries.one('total_counts')['events'] == 2
    assert queries.one('invitation_totals')['active'] == 2
    assert queries.rows('invitations_by_event')[0]['invitation_count'] == 2
    assert [row['name'] for row in queries.rows('available_guests', (1,))] == [
        'Иван', 'Мария'
    ]
    assert len(queries.rows('invitations_by_status', ('active',))) == 2
    assert not queries.rows('invitations_by_status', ("active' OR 1=1 --",))


@pytest.mark.parametrize('view_name', [
    'homepage:index', 'events:list', 'invitations:list', 'users:list', 'guests:list',
    'events:search', 'events:available', 'invitations:statistics',
])
def test_page_is_rendered(sqlite_db, view_name):
    response = Client().get(reverse(view_name))
    assert response.status_code == 200
    assert b'<html' in response.content


def test_search_and_statistics(sqlite_db):
    client = Client()
    assert 'Новогодняя встреча' in client.get(
        reverse('events:search'), {'date': '2026-12-28'}
    ).content.decode('utf-8')
    assert 'Иван' in client.get(
        reverse('events:available'), {'event_id': 1}
    ).content.decode('utf-8')
    assert 'Активных' in client.get(
        reverse('invitations:statistics')
    ).content.decode('utf-8')
    assert 'Анна' in client.get(
        reverse('invitations:list'), {'status': 'active'}
    ).content.decode('utf-8')


@pytest.mark.parametrize('name', [
    'events:detail', 'invitations:detail', 'users:detail', 'guests:detail',
])
def test_missing_object_404(sqlite_db, name):
    with override_settings(DEBUG=False, ALLOWED_HOSTS=['testserver']):
        response = Client().get(reverse(name, args=[999]))
        assert response.status_code == 404
        assert 'Страница не найдена' in response.content.decode('utf-8')


def test_unmatched_route_404(sqlite_db):
    with override_settings(DEBUG=False, ALLOWED_HOSTS=['testserver']):
        response = Client().get('/route-that-does-not-exist/')
    assert response.status_code == 404
    assert '404' in response.content.decode('utf-8')


def test_error_handlers_and_templates(sqlite_db):
    request = RequestFactory().get('/error-test/')
    for code, handler in (
        (400, error_views.bad_request), (403, error_views.permission_denied),
        (404, error_views.page_not_found),
    ):
        response = handler(request, Exception('не показывать пользователю'))
        assert response.status_code == code
        assert str(code) in response.content.decode('utf-8')
        assert 'не показывать пользователю' not in response.content.decode('utf-8')
        get_template(f'{code}.html')
    response = error_views.server_error(request)
    assert response.status_code == 500
    assert '500' in response.content.decode('utf-8')
    get_template('500.html')
