from django.test import TestCase
from django.urls import reverse

from ..models import IndirectInput, DirectInput
from .create_objects import create_patient, create_user


class TestInputs(TestCase):

    def setUp(self):
        self.client = create_user()
        self.patient = create_patient(1)

    def test_direct_input_get(self):
        response = self.client.get(reverse('OPAL:direct_input_create', args=[self.patient.id]))
        self.assertEqual(response.status_code, 200)

    def test_direct_input_post(self):
        direct_input = DirectInput.objects.create(id=1, title="test")
        response = self.client.post(reverse('OPAL:direct_input_create', args=[self.patient.id]), data=direct_input.__dict__)
        self.assertEqual(response.status_code, 302)

    def test_indirect_input_get(self):
        response = self.client.get(reverse('OPAL:indirect_input_create', args=[self.patient.id]))
        self.assertEqual(response.status_code, 200)

    def test_indirect_input_post(self):
        indirect_input = IndirectInput.objects.create(id=1, title="test")
        response = self.client.post(reverse('OPAL:indirect_input_create', args=[self.patient.id]), data=indirect_input.__dict__)
        self.assertEqual(response.status_code, 302)
