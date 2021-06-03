from django.test import TestCase
from django.urls import reverse

from ..models import Patient
from .create_objects import create_user, create_patient


class TestPatients(TestCase):

    def setUp(self):
        self.client = create_user()

    def test_patient_list(self):
        response = self.client.get(reverse('OPAL:patient_list'))
        self.assertEqual(response.status_code, 200)

    def test_patient_create_get(self):
        response = self.client.get(reverse('OPAL:patient_create'))
        self.assertEqual(response.status_code, 200)

    def test_patient_create_post(self):
        patient = create_patient(1)
        response = self.client.post(reverse('OPAL:patient_create'), data=patient.__dict__)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Patient.objects.first().first_name, 'john')

    def test_patient_edit_get(self):
        patient = create_patient(1)
        self.client.post(reverse('OPAL:patient_create'), data=patient.__dict__)
        response = self.client.get(reverse('OPAL:patient_edit', args=[patient.id]))
        self.assertEqual(response.status_code, 200)

    def test_patient_edit_post(self):
        patient = create_patient(1)
        self.client.post(reverse('OPAL:patient_create'), data=patient.__dict__)
        response = self.client.post(reverse('OPAL:patient_edit', args=[patient.id]), data=patient.__dict__)
        self.assertEqual(response.status_code, 200)

    def test_patient_delete(self):
        patient = create_patient(1)
        self.client.post(reverse('OPAL:patient_create'), data=patient.__dict__)
        response = self.client.post(reverse('OPAL:patient_delete', args=[patient.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Patient.objects.count(), 0)
