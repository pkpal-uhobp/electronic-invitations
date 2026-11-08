from django.test import TestCase
from django.urls import reverse
from .models import Guest


class GuestTests(TestCase):
    def test_list_and_404(self):
        Guest.objects.create(name='Тест', email='test@example.com')
        self.assertEqual(self.client.get(reverse('guests:list')).status_code, 200)
        self.assertEqual(self.client.get(reverse('guests:detail', args=[999])).status_code, 404)
