from django.test import TestCase
from ..forms import PatientUserForm

class FormTests(TestCase):

    def test_patient_user_form_valid(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'password': 'password123'
        }
        form = PatientUserForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_patient_user_form_invalid(self):
        form = PatientUserForm(data={})
        self.assertFalse(form.is_valid())