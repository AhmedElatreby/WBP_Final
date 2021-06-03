from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client

from OPAL.models import Patient, Therapist, Team
from ..models import Pathway, ReferralSource


class TestPathway(TestCase):

    def setUp(self):
        self.client = Client()
        password = "testpass"
        admin = User.objects.create_superuser("tester", "myemail@test.com", password)
        self.client.login(username=admin.username, password=password)
        self.patient = Patient.objects.create(id=1, first_name="john", surname="smith", date_of_birth="1995-10-09",
                                              hospital_number="10293", postcode="tester", locality="Poole")
        self.rs = ReferralSource.objects.create(id=1, name="test")
        self.therapist = Therapist.objects.create(id=1, first_name="john", surname="smith", assigned_team=Team.objects.create(id=1, team_name="test"))
        self.pathway = Pathway.objects.create(id=1, patient=self.patient, admission_date="1995-09-10", referral_source=self.rs, meet_criteria_therapy=True,
                                              front_door=True, RAFT=True, CCMT=True, CCMT_date="1995-09-10", admission_barthel=2, discharge_barthel=1)

    def test_pathway_list(self):
        response = self.client.get(reverse('services:pathway_list', args=[self.patient.id]))
        self.assertEqual(response.status_code, 200)

    def test_pathway_delete(self):
        self.client.post(reverse('services:pathway_create', args=[self.patient.id]), data=self.pathway.__dict__)
        response = self.client.post(reverse('services:pathway_delete', args=[self.pathway.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Pathway.objects.count(), 0)

    def test_pathway_create_get(self):
        response = self.client.get(reverse('services:pathway_create', args=[self.patient.id]), args=[self.patient.id])
        self.assertEqual(response.status_code, 200)

    def test_pathway_create_post(self):
        response = self.client.post(reverse('services:pathway_create', args=[self.patient.id]), data=self.pathway.__dict__)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Pathway.objects.first().id, 1)

    def test_referral_source_create_get(self):
        response = self.client.get(reverse('services:referral_source_create', args=[self.patient.id]), data=self.rs.__dict__)
        self.assertEqual(response.status_code, 200)

    def test_referral_source_create_post(self):
        response = self.client.post(reverse('services:referral_source_create', args=[self.patient.id]), data=self.rs.__dict__)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ReferralSource.objects.first().id, 1)

    def test_pathway_edit_get(self):
        self.client.post(reverse('services:pathway_create', args=[self.patient.id]), data=self.pathway.__dict__)
        response = self.client.get(reverse('services:pathway_edit', args=[self.pathway.id]))
        self.assertEqual(response.status_code, 200)

    def test_pathway_edit_post(self):
        self.client.post(reverse('services:pathway_create', args=[self.patient.id]), data=self.pathway.__dict__)
        response = self.client.post(reverse('services:pathway_edit', args=[self.pathway.id]), data=self.pathway.__dict__)
        self.assertEqual(response.status_code, 200)
