"""Smoke test: earlier console and JSON functions remain intact."""
from datetime import date, timedelta

from events import add_event, find_events
from invitations import add_invitation, cancel_invitation, is_invitation_available
from models import Event, Guest, User
from storage import load_events, load_guests, load_invitations, load_users


def test_old_console_behaviour():
    values = {}
    ident = add_event(values, 'Тест', date.today() + timedelta(days=2))
    assert ident == '1'
    assert find_events(values, 'Тест')
    invitations = []
    item = add_invitation(invitations, '1', 'Анна')
    assert not is_invitation_available(invitations, '1', 'Анна')
    assert cancel_invitation(invitations, item['id'])
    assert is_invitation_available(invitations, '1', 'Анна')


def test_old_models_and_storage():
    users, guests = load_users(), load_guests()
    events = load_events(users)
    invitations = load_invitations(events, guests)
    assert len(users) == 2 and isinstance(users[0], User)
    assert len(guests) == 3 and isinstance(guests[0], Guest)
    assert len(events) == 2 and isinstance(events[0], Event)
    assert len(invitations) == 3
