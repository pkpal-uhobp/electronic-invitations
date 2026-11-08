from django.test import TestCase
from django.urls import reverse
from .models import User


class OrganizerTests(TestCase):
    def test_list_and_404(self):
        User.objects.create(name='Тест', email='test@example.com')
        self.assertEqual(self.client.get(reverse('users:list')).status_code, 200)
        self.assertEqual(self.client.get(reverse('users:detail', args=[999])).status_code, 404)
