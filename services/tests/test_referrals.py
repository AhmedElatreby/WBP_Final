from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client

from OPAL.models import Patient, Therapist, Team
from ..models import Referral


class TestReferrals(TestCase):

    def setUp(self):
        self.client = Client()
        password = "testpass"
        admin = User.objects.create_superuser("tester", "myemail@test.com", password)
        self.client.login(username=admin.username, password=password)
        self.patient = Patient.objects.create(id=1, first_name="john", surname="smith", date_of_birth="1995-10-09",
                                              hospital_number="10293", postcode="tester", locality="Poole")
        self.therapist = Therapist.objects.create(id=1, first_name="john", surname="smith", assigned_team=Team.objects.create(id=1, team_name="test"))
        self.referral = Referral.objects.create(id=1, patient=self.patient, therapist_referring=self.therapist, referral_date="1995-09-10", initial_contact_date="1995-09-10")

    def test_referral_list(self):
        response = self.client.get(reverse('services:referral_list', args=[self.patient.id]))
        self.assertEqual(response.status_code, 200)

    def test_referral_delete(self):
        self.client.post(reverse('services:referral_create', args=[self.patient.id]), data=self.referral.__dict__)
        response = self.client.post(reverse('services:referral_delete', args=[self.referral.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Referral.objects.count(), 0)

    def test_referral_create_get(self):
        response = self.client.get(reverse('services:referral_create', args=[self.patient.id]), args=[self.patient.id])
        self.assertEqual(response.status_code, 200)

    def test_referral_create_post(self):
        response = self.client.post(reverse('services:referral_create', args=[self.patient.id]), data=self.referral.__dict__)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Referral.objects.first().id, 1)

    def test_referral_edit_get(self):
        self.client.post(reverse('services:referral_create', args=[self.patient.id]), data=self.referral.__dict__)
        response = self.client.get(reverse('services:referral_edit', args=[self.referral.id]))
        self.assertEqual(response.status_code, 200)

    def test_referral_edit_post(self):
        self.client.post(reverse('services:referral_create', args=[self.patient.id]), data=self.referral.__dict__)
        response = self.client.post(reverse('services:referral_edit', args=[self.referral.id]), data=self.referral.__dict__)
        self.assertEqual(response.status_code, 200)
