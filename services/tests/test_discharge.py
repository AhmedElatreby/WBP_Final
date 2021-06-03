from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client

from OPAL.models import Patient, Therapist, Team
from ..models import DischargeService, Discharge


class TestDischarge(TestCase):

    def setUp(self):
        self.client = Client()
        password = "testpass"
        admin = User.objects.create_superuser("tester", "myemail@test.com", password)
        self.client.login(username=admin.username, password=password)
        self.patient = Patient.objects.create(id=1, first_name="john", surname="smith", date_of_birth="1995-10-09",
                                              hospital_number="10293", postcode="tester", locality="Poole")
        self.therapist = Therapist.objects.create(id=1, first_name="john", surname="smith", assigned_team=Team.objects.create(id=1, team_name="test"))
        self.discharge_service = DischargeService.objects.create(id=1, name="test", description="test")
        self.discharge = Discharge.objects.create(id=1, patient=self.patient, date_no_reside="1995-09-10", discharge_date="1995-09-10",
                                                  discharge_service=self.discharge_service, delay_reason="test")

    def test_discharge_list(self):
        response = self.client.get(reverse('services:discharge_list', args=[self.patient.id]))
        self.assertEqual(response.status_code, 200)

    def test_discharge_delete(self):
        self.client.post(reverse('services:discharge_create', args=[self.patient.id]), data=self.discharge.__dict__)
        response = self.client.post(reverse('services:discharge_delete', args=[self.discharge.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Discharge.objects.count(), 0)

    def test_discharge_create_get(self):
        response = self.client.get(reverse('services:discharge_create', args=[self.patient.id]), args=[self.patient.id])
        self.assertEqual(response.status_code, 200)

    def test_discharge_create_post(self):
        response = self.client.post(reverse('services:discharge_create', args=[self.patient.id]), data=self.discharge.__dict__)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Discharge.objects.first().id, 1)

    def test_discharge_service_create_get(self):
        response = self.client.get(reverse('services:discharge_service_create', args=[self.patient.id]), data=self.discharge_service.__dict__)
        self.assertEqual(response.status_code, 200)

    def test_discharge_service_create_post(self):
        response = self.client.post(reverse('services:discharge_service_create', args=[self.patient.id]), data=self.discharge_service.__dict__)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Discharge.objects.first().id, 1)

    def test_discharge_edit_get(self):
        self.client.post(reverse('services:discharge_create', args=[self.patient.id]), data=self.discharge.__dict__)
        response = self.client.get(reverse('services:discharge_edit', args=[self.discharge.id]))
        self.assertEqual(response.status_code, 200)

    def test_discharge_edit_post(self):
        self.client.post(reverse('services:discharge_create', args=[self.patient.id]), data=self.discharge.__dict__)
        response = self.client.post(reverse('services:discharge_edit', args=[self.discharge.id]), data=self.discharge.__dict__)
        self.assertEqual(response.status_code, 200)
