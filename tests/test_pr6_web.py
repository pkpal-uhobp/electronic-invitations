"""Интеграционные тесты ПР6. Запускаются при установленном Django 5.2."""
import os
import pytest

django = pytest.importorskip('django')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inviteweb.settings')
django.setup()
from django.test import Client
from django.urls import reverse
from django.template.loader import get_template
from django.contrib.staticfiles import finders


@pytest.fixture
def client():
    return Client()


@pytest.mark.parametrize('name', [
    'homepage:index', 'events:list', 'invitations:list', 'users:list', 'guests:list',
])
def test_list_pages_render(client, name):
    response = client.get(reverse(name))
    assert response.status_code == 200
    assert b'<html' in response.content


@pytest.mark.parametrize('name', [
    'events:detail', 'invitations:detail', 'users:detail', 'guests:detail',
])
def test_detail_pages(client, name):
    assert client.get(reverse(name, args=[1])).status_code == 200
    assert client.get(reverse(name, args=[999])).status_code == 404


def test_named_links_present_on_home(client):
    html = client.get('/').content.decode('utf-8')
    assert '/events/' in html
    assert '/invitations/' in html
    assert '/users/' in html
    assert '/guests/' in html


def test_templates_and_static_files_exist():
    get_template('base.html')
    get_template('events_web/event_list.html')
    get_template('invitations_web/invitation_detail.html')
    get_template('users_web/user_detail.html')
    get_template('guests_web/guest_detail.html')
    assert finders.find('homepage/css/style.css')
    assert finders.find('homepage/js/main.js')
    assert finders.find('homepage/img/logo.png')
