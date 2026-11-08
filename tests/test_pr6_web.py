"""PR6 named routing/templates/static resources retained by PR9."""
from django.test import Client
from django.template.loader import get_template
from django.contrib.staticfiles import finders
from django.urls import reverse
import pytest

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize('name', [
    'homepage:index', 'events:list', 'invitations:list', 'users:list', 'guests:list',
    'events:search', 'events:available', 'invitations:statistics',
])
def test_list_pages_render(name):
    response = Client().get(reverse(name))
    assert response.status_code == 200
    assert b'<html' in response.content


def test_templates_and_static():
    for template in ('base.html', 'events_web/event_list.html',
                     'invitations_web/invitation_detail.html',
                     'users_web/user_detail.html', 'guests_web/guest_detail.html'):
        get_template(template)
    for name in ('homepage/css/style.css', 'homepage/css/pr7.css',
                 'homepage/css/pr9.css', 'homepage/js/main.js', 'homepage/img/logo.png'):
        assert finders.find(name)
