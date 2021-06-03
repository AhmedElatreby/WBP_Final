from django.test import TestCase
from django.urls import reverse

from ..models import Therapist
from .create_objects import create_user, create_team, create_therapist


class TestTherapists(TestCase):

    def setUp(self):
        self.client = create_user()

    def test_therapist_list(self):
        response = self.client.get(reverse('OPAL:therapist_list'))
        self.assertEqual(response.status_code, 200)

    def test_therapist_create_get(self):
        response = self.client.get(reverse('OPAL:therapist_create'))
        self.assertEqual(response.status_code, 200)

    def test_therapist_create_post(self):
        team = create_team(1)
        therapist = create_therapist(1, team)
        response = self.client.post(reverse('OPAL:therapist_create'), data=therapist.__dict__)
        self.assertEqual(response.status_code, 200)

    def test_assigned_team_get(self):
        response = self.client.get(reverse('OPAL:assigned_team_create'))
        self.assertEqual(response.status_code, 200)

    def test_assigned_team_post(self):
        team = create_team(1)
        response = self.client.post(reverse('OPAL:assigned_team_create'), data=team.__dict__)
        self.assertEqual(response.status_code, 302)

    def test_therapist_edit_get(self):
        team = create_team(1)
        therapist = create_therapist(1, team)
        self.client.post(reverse('OPAL:therapist_create'), data=therapist.__dict__)
        response = self.client.get(reverse('OPAL:therapist_edit', args=[therapist.id]))
        self.assertEqual(response.status_code, 200)

    def test_therapist_edit_post(self):
        team = create_team(1)
        therapist = create_therapist(1, team)
        self.client.post(reverse('OPAL:therapist_create'), data=therapist.__dict__)
        response = self.client.post(reverse('OPAL:therapist_edit', args=[therapist.id]), data=therapist.__dict__)
        self.assertEqual(response.status_code, 200)

    def test_therapist_delete(self):
        team = create_team(1)
        therapist = create_therapist(1, team)
        self.client.post(reverse('OPAL:therapist_create'), data=therapist.__dict__)
        response = self.client.post(reverse('OPAL:therapist_delete', args=[therapist.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Therapist.objects.count(), 0)
