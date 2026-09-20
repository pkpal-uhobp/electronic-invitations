import pytest

from invitations import (
    add_invitation,
    cancel_invitation,
    invitation_statistics,
    is_invitation_available,
    set_response,
)


def test_add_invitation_blocks_duplicate_active_invitation() -> None:
    invitations: list[dict[str, str]] = []
    add_invitation(invitations, "1", "Анна")

    assert not is_invitation_available(invitations, "1", "Анна")
    with pytest.raises(ValueError):
        add_invitation(invitations, "1", "Анна")


def test_cancel_invitation_allows_new_invitation() -> None:
    invitations: list[dict[str, str]] = []
    invitation = add_invitation(invitations, "1", "Анна")

    assert cancel_invitation(invitations, invitation["id"])
    assert is_invitation_available(invitations, "1", "Анна")


def test_set_response_and_statistics() -> None:
    invitations: list[dict[str, str]] = []
    invitation = add_invitation(invitations, "1", "Иван")

    assert set_response(invitations, invitation["id"], "да")
    statistics = invitation_statistics(invitations)

    assert statistics["active"] == 1
    assert statistics["yes"] == 1
    assert statistics["unknown"] == 0


def test_invalid_response_raises_error() -> None:
    invitations: list[dict[str, str]] = []
    invitation = add_invitation(invitations, "1", "Иван")

    with pytest.raises(ValueError):
        set_response(invitations, invitation["id"], "может быть")
