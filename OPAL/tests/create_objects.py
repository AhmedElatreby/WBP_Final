from ..models import Team, Therapist, Therapy, Patient, DirectInput, IndirectInput
from django.test import Client
from django.contrib.auth.models import User


def create_team(id):
    return Team.objects.create(id=id, team_name="test")


def create_therapist(id, team):
    return Therapist.objects.create(id=id, first_name="john", surname="smith", assigned_team=team)


def create_patient(id):
    return Patient.objects.create(id=id, first_name="john", surname="smith", date_of_birth="1995-10-09",
                                  hospital_number="10293", postcode="tester", locality="Poole")


def create_user():
    client = Client()
    password = "testpass"
    admin = User.objects.create_superuser("tester", "myemail@test.com", password)
    client.login(username=admin.username, password=password)
    return client


def create_therapy():
    team = create_team(1)
    patient = create_patient(1)
    therapist = create_therapist(1, team)
    indirect_input = IndirectInput.objects.create(id=1, title="test")
    direct_input = DirectInput.objects.create(id=1, title="test")
    return Therapy.objects.create(id=1, patient=patient, therapist=therapist, indirect_input=indirect_input, 
                                  direct_input=direct_input, direct_time=20, indirect_time=20)
