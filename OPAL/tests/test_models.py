from django.test import TestCase
from django.urls import reverse

from ..models import IndirectInput, DirectInput
from .create_objects import create_user, create_team, create_therapist, create_patient, create_therapy


class ModelsTest(TestCase):

    def setUp(self):
        self.client = create_user()

    def test_team_string_value(self):
        team = create_team(1)
        self.assertEqual("test", str(team))

    def test_therapist_string_value(self):
        team = create_team(1)
        therapist = create_therapist(1, team)
        self.assertEqual("john smith: 1", str(therapist))

    def test_therapist_absolute_url(self):
        team = create_team(1)
        therapist = create_therapist(1, team)
        response = self.client.get(reverse('OPAL:therapist_single', args=[therapist.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(reverse('OPAL:therapist_single', args=[therapist.id])), therapist.get_absolute_url())

    def test_patient_string_value(self):
        patient = create_patient(1)
        self.assertEqual("john smith: 10293", str(patient))

    def test_patient_absolute_url(self):
        patient = create_patient(1)
        response = self.client.get(reverse('OPAL:patient_single', args=[patient.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(reverse('OPAL:patient_single', args=[patient.id])), patient.get_absolute_url())

    def test_therapy_string_value(self):
        therapy = create_therapy()
        self.assertEqual("1", str(therapy))

    def test_therapy_absolute_url(self):
        therapy = create_therapy()
        response = self.client.get(reverse('OPAL:therapy_single', args=[therapy.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(reverse('OPAL:therapy_single', args=[therapy.id])), therapy.get_absolute_url())

    def test_indirect_input_string_value(self):
        indirect_input = IndirectInput.objects.create(id=1, title="test")
        self.assertEqual("test", str(indirect_input))

    def test_direct_input_string_value(self):
        direct_input = DirectInput.objects.create(id=1, title="test")
        self.assertEqual("test", str(direct_input))
