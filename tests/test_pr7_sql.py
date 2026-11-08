"""Legacy PR7 SQL is preserved, even though PR9 Django views no longer use it."""
from pathlib import Path
import pytest
from db import database, queries
from db.import_json import import_json


@pytest.fixture
def sqlite_db(tmp_path, monkeypatch):
    path = tmp_path / 'invitations.sqlite'
    import_json(Path(__file__).resolve().parent.parent / 'data', path)
    monkeypatch.setattr(database, 'DB_PATH', path)
    return path


def test_legacy_sql_schema_and_queries(sqlite_db):
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
    assert queries.one('total_counts')['invitations'] == 3
    assert queries.one('invitation_totals')['active'] == 2
    assert queries.rows('available_guests', (1,))[0]['name'] == 'Иван'


def test_legacy_import_can_be_repeated(sqlite_db):
    data_dir = Path(__file__).resolve().parent.parent / 'data'
    import_json(data_dir, sqlite_db)
    import_json(data_dir, sqlite_db)
    assert queries.one('total_counts')['invitations'] == 3
