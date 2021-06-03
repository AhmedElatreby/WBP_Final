from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse
from OPAL.models import Patient


class TestInputs(TestCase):

    def setUp(self):
        self.patient = Patient.objects.create(id=1, first_name="john", surname="smith", date_of_birth="1995-10-09",
                                              hospital_number="10293", postcode="tester", locality="Poole")
        self.client = Client()
        password = "testpass"
        admin = User.objects.create_superuser("tester", "myemail@test.com", password)
        self.client.login(username=admin.username, password=password)

    def test_add_service_get(self):
        response = self.client.get(reverse('services:add_service', args=[self.patient.id]))
        self.assertEqual(response.status_code, 200)

    def test_view_services_get(self):
        response = self.client.get(reverse('services:view_services', args=[self.patient.id]))
        self.assertEqual(response.status_code, 200)
