"""Django-native event checks."""
from datetime import date

from django.test import TestCase
from django.urls import reverse

from .models import Event


class EventORMTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.event = Event.objects.create(name='Тест', date=date(2027, 1, 2))

    def test_search(self):
        response = self.client.get(reverse('events:search'), {'date': '2027-01-02'})
        self.assertEqual(len(response.context['events']), 1)

    def test_invalid_date(self):
        response = self.client.get(reverse('events:search'), {'date': 'bad'})
        self.assertTrue(response.context['error'])

    def test_missing_event(self):
        self.assertEqual(self.client.get(reverse('events:detail', args=[999])).status_code, 404)
