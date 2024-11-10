from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Doctor, Patient

class ModelTests(TestCase):

    def setUp(self):
        self.doctor = Doctor.objects.create(
            user=User.objects.create_user(username="doctoruser", first_name="testdoctor", last_name="test", password="password"),
            department="Cardiologist", address="123 Doctor St.", mobile="1234567890"
        )
        self.patient = Patient.objects.create(
            user=User.objects.create_user(username="patientuser", first_name="testpatient", last_name="test", password="password"),
            symptoms="Test symptoms", address="456 Patient St.", mobile="0987654321"
        )

    def test_doctor_str(self):
        self.assertEqual(str(self.doctor), "testdoctor (Cardiologist)")

    def test_patient_str(self):
        self.assertEqual(str(self.patient), "testpatient (Test symptoms)")
