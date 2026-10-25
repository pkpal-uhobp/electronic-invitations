"""Адаптация sqlite3.Row в прежние предметные модели для Django-шаблонов ПР6.

SQL остаётся в sql/queries.sql; старые Python-модели и консольный JSON-код не меняются.
"""
from models import Event, Guest, Invitation, User
from . import queries


def user_from_row(row):
    return User(str(row['id']), row['name'], row['email'])


def guest_from_row(row):
    return Guest(str(row['id']), row['name'], row['email'])


def event_from_row(row):
    organizer = None
    if row['user_id'] is not None and row['organizer_name'] is not None:
        organizer = User(str(row['user_id']), row['organizer_name'], row['organizer_email'])
    return Event(str(row['id']), row['name'], row['date'], organizer)


def invitation_from_row(row):
    event = Event(str(row['event_id']), row['event_name'], row['event_date'])
    if row['guest_id'] is not None and row['guest_real_name'] is not None:
        guest = Guest(str(row['guest_id']), row['guest_real_name'], row['guest_email'])
    else:
        guest = row['guest_name']
    invite = Invitation(str(row['id']), event, guest)
    invite.response = row['response']
    invite.status = row['status']
    return invite


def events(name='events_list', params=()):
    return [event_from_row(row) for row in queries.rows(name, params)]


def invitations(name='invitations_list', params=()):
    return [invitation_from_row(row) for row in queries.rows(name, params)]


def users():
    return [user_from_row(row) for row in queries.rows('users_list')]


def guests():
    return [guest_from_row(row) for row in queries.rows('guests_list')]
