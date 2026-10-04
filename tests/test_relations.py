from models import Guest
from storage import load_events, load_guests, load_invitations, load_users


def test_event_user_and_invitation_guest_relations() -> None:
    users = load_users()
    guests = load_guests()
    events = load_events(users)
    invitations = load_invitations(events, guests)

    assert events[0].user is not None
    assert events[0].user.id == "1"
    assert isinstance(invitations[0].guest, Guest)
    assert invitations[0].guest.id == "1"
