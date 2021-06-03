from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User

from ..models import ReferralSource, Pathway, D2A, Referral, DischargeService, Discharge
from OPAL.models import Patient, Therapist, Team


class ModelsTest(TestCase):

    def setUp(self):
        self.client = Client()
        password = "testpass"
        admin = User.objects.create_superuser("tester", "myemail@test.com", password)
        self.client.login(username=admin.username, password=password)
        self.patient = Patient.objects.create(id=1, first_name="john", surname="smith", date_of_birth="1995-10-09",
                                              hospital_number="10293", postcode="tester", locality="Poole")
        self.rs = ReferralSource.objects.create(id=1, name="test")
        self.therapist = Therapist.objects.create(id=1, first_name="john", surname="smith", assigned_team=Team.objects.create(id=1, team_name="test"))
        self.discharge_service = DischargeService.objects.create(id=1, name="test", description="test")

    def test_referral_source_string_value(self):
        self.assertEqual("test", str(self.rs))

    def test_pathway_string_value(self):
        pathway = Pathway.objects.create(id=1, patient=self.patient, admission_date="1995-09-10", referral_source=self.rs)
        self.assertEqual("john smith: Pathway", str(pathway))

    def test_D2A_string_value(self):
        d2a = D2A.objects.create(id=1, patient=self.patient, therapist_completing_D2A=self.therapist, D2A_completion_date="1995-09-10")
        self.assertEqual("john smith: D2A", str(d2a))

    def test_referral_string_value(self):
        referral = Referral.objects.create(id=1, patient=self.patient, therapist_referring=self.therapist, referral_date="1995-09-10", initial_contact_date="1995-09-10")
        self.assertEqual("john smith: Referral", str(referral))

    def test_discharge_service_string_value(self):
        self.assertEqual("test - test", str(self.discharge_service))

    def test_discharge_string_value(self):
        discharge = Discharge.objects.create(id=1, patient=self.patient, date_no_reside="1995-09-10", discharge_date="1995-09-10", discharge_service=self.discharge_service)
        self.assertEqual("john smith: Discharge", str(discharge))
