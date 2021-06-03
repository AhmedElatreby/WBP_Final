from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse


class TestInputs(TestCase):

    def setUp(self):
        self.client = Client()
        password = "testpass"
        admin = User.objects.create_user("tester", "myemail@test.com", password)
        self.client.login(username=admin.username, password=password)

    def test_home_get(self):
        response = self.client.get(reverse('navigation:home'))
        self.assertEqual(response.status_code, 200)

    def test_options_post(self):
        response = self.client.post(reverse('navigation:options'))
        self.assertEqual(response.status_code, 200)