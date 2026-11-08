"""Homepage uses the ORM even when database is empty."""
from django.test import TestCase
from django.urls import reverse


class HomepageTests(TestCase):
    def test_homepage(self):
        response = self.client.get(reverse('homepage:index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['stats']['events'], 0)
