from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Patient, Doctor  # Ensure this is correct

class ViewTests(TestCase):

    def setUp(self):
        
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')  # Log in the user

    def test_home_view(self):
        response = self.client.get(reverse('home_view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hospital/index.html')

