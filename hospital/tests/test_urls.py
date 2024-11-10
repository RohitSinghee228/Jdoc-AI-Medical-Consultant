from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ..views import  patient_dashboard_view

class UrlsTests(SimpleTestCase):

    def test_patient_dashboard_url_resolves(self):
        url = reverse('patient-dashboard')
        self.assertEqual(resolve(url).func, patient_dashboard_view)