"""Django-native regression tests (discoverable by manage.py test)."""
from datetime import date

from django.test import TestCase
from django.urls import reverse

from events_web.models import Event
from guests_web.models import Guest
from users_web.models import User
from .models import Invitation


class InvitationORMTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.organizer = User.objects.create(name='Организатор', email='org@example.com')
        cls.guest = Guest.objects.create(name='Анна', email='anna@example.com')
        cls.event = Event.objects.create(
            name='День рождения', date=date(2027, 1, 1), user=cls.organizer)
        cls.invitation = Invitation.objects.create(
            event=cls.event, guest=cls.guest, guest_name=cls.guest.name, response='да')

    def test_related_objects(self):
        self.assertEqual(self.organizer.events.count(), 1)
        self.assertEqual(self.event.invitations.count(), 1)
        self.assertEqual(self.guest.invitations.count(), 1)

    def test_list_detail_stats(self):
        self.assertEqual(self.client.get(reverse('invitations:list')).status_code, 200)
        self.assertEqual(self.client.get(reverse('invitations:detail', args=[
            self.invitation.pk])).status_code, 200)
        self.assertEqual(self.client.get(reverse('invitations:detail', args=[
            999])).status_code, 404)
        response = self.client.get(reverse('invitations:statistics'))
        self.assertEqual(response.context['totals']['total'], 1)
        self.assertEqual(response.context['totals']['active'], 1)

    def test_crud(self):
        item = Invitation.objects.get(pk=self.invitation.pk)
        item.set_response('нет')
        item.cancel()
        item.refresh_from_db()
        self.assertEqual(item.status, 'cancelled')
        self.assertEqual(item.response, 'нет')
        item.delete()
        self.assertFalse(Invitation.objects.filter(pk=item.pk).exists())

    def test_filtered_list(self):
        result = self.client.get(reverse('invitations:list'), {'status': 'active'})
        self.assertEqual(result.context['page_obj'].paginator.count, 1)
        result = self.client.get(reverse('invitations:list'), {'q': 'День'})
        self.assertEqual(result.context['page_obj'].paginator.count, 1)
