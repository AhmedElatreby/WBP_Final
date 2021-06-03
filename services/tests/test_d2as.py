from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client

from OPAL.models import Patient, Therapist, Team
from ..models import DischargeService, ReferralSource, D2A


class TestD2As(TestCase):

    def setUp(self):
        self.client = Client()
        password = "testpass"
        admin = User.objects.create_superuser("tester", "myemail@test.com", password)
        self.client.login(username=admin.username, password=password)
        self.patient = Patient.objects.create(id=1, first_name="john", surname="smith", date_of_birth="1995-10-09",
                                              hospital_number="10293", postcode="tester", locality="Poole")
        self.rs = ReferralSource.objects.create(id=1, name="test")
        self.therapist = Therapist.objects.create(id=1, first_name="john", surname="smith", assigned_team=Team.objects.create(id=1, team_name="test"))
        self.d2a = D2A.objects.create(id=1, patient=self.patient, therapist_completing_D2A=self.therapist, D2A_completion_date="1995-09-10")
        self.discharge_service = DischargeService.objects.create(id=1, name="test", description="test")

    def test_d2a_list(self):
        response = self.client.get(reverse('services:D2A_list', args=[self.patient.id]))
        self.assertEqual(response.status_code, 200)

    def test_d2a_delete(self):
        self.client.post(reverse('services:D2A_create', args=[self.patient.id]), data=self.d2a.__dict__)
        response = self.client.post(reverse('services:D2A_delete', args=[self.d2a.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(D2A.objects.count(), 0)

    def test_d2a_create_get(self):
        response = self.client.get(reverse('services:D2A_create', args=[self.patient.id]), args=[self.patient.id])
        self.assertEqual(response.status_code, 200)

    def test_d2a_create_post(self):
        response = self.client.post(reverse('services:D2A_create', args=[self.patient.id]), data=self.d2a.__dict__)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(D2A.objects.first().id, 1)

    def test_d2a_edit_get(self):
        self.client.post(reverse('services:D2A_create', args=[self.patient.id]), data=self.d2a.__dict__)
        response = self.client.get(reverse('services:D2A_edit', args=[self.d2a.id]))
        self.assertEqual(response.status_code, 200)

    def test_d2a_edit_post(self):
        self.client.post(reverse('services:D2A_create', args=[self.patient.id]), data=self.d2a.__dict__)
        response = self.client.post(reverse('services:D2A_edit', args=[self.d2a.id]), data=self.d2a.__dict__)
        self.assertEqual(response.status_code, 200)
