from django.db import models
from OPAL.models import Patient, Therapist


# Create the Referral Source model in the database:
# Listed fields:
# - name: The name of the referral source
class ReferralSource(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# Create the pathway model in the database:
# Listed fields:
# - patient: The patient who is going through the pathway
# - admission_date: The admission date of the pathway
# - meet_criteria_therapy: Does this pathway meet criteria for therapy
# - referral_source: Where did the referral come from
# - front_door: Was this pathway through front door
# - RAFT: IS this pathway RAFT
# - CCMT: Was this pathway CCMT
# - CCMT_Date: What was the date of CCMT if it happened
# - admission_barthel: level of admission
# - discharge_barthel: level of discharge
# - created_at: When the pathway was created
# - updated_at: when the pathway was updated
class Pathway(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    admission_date = models.DateField()
    meet_criteria_therapy = models.BooleanField(default=False)
    referral_source = models.ForeignKey(ReferralSource, on_delete=models.CASCADE)
    front_door = models.BooleanField(default=False)
    RAFT = models.BooleanField(default=False)
    CCMT = models.BooleanField(default=False)
    CCMT_date = models.DateField(blank=True, null=True)
    admission_barthel = models.IntegerField(blank=True, null=True)
    discharge_barthel = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.patient.first_name} {self.patient.surname}: Pathway"


# Create the D2A model in the database:
# Listed fields:
# - patient: The patient who is D2A
# - therapist_completing_d2a: the therapist completing the d2a
# - D2A_completion_date: When the d2a was completed
# - created_at: When the D2A was created
# - updated_at: when the D2A was updated
class D2A(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    therapist_completing_D2A = models.ForeignKey(Therapist, on_delete=models.CASCADE)
    D2A_completion_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.patient.first_name} {self.patient.surname}: D2A"


# Create the referral model in the database:
# Listed fields:
# - patient: The patient who is referred
# - type_of_referral: The referral type
# - therapist_referring: Who is making the referral
# - referral_date: The date of the referral
# - initial_contact_date: When the patient was initially referred
# - created_at: When the referral was created
# - updated_at: when the referral was updated
class Referral(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    type_of_referral = models.CharField(max_length=50)
    therapist_referring = models.ForeignKey(Therapist, on_delete=models.CASCADE)
    referral_date = models.DateField()
    initial_contact_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.patient.first_name} {self.patient.surname}: Referral"


# Create the discharge service model in the database:
# Listed fields:
# - name: the name of the discharge service
# - description: The description of this discharge service
class DischargeService(models.Model):
    name = models.CharField(max_length=10)
    description = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} - {self.description}"


# Create the referral model in the database:
# Listed fields:
# - patient: The patient who is referred
# - date_no_reside: The date of the leave of reside
# - discharge_date: The date of the discharge
# - discharge_service: The service making the discharge
# - delay_discharge: Any delays to the discharge
# - delay_reason: The reson for delay
# - created_at: When the discharge was created
# - updated_at: when the discharge was updated
class Discharge(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date_no_reside = models.DateField()
    discharge_date = models.DateField()
    discharge_service = models.ForeignKey(DischargeService, on_delete=models.CASCADE)
    delay_discharge = models.BooleanField(default=False)
    delay_reason = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.patient.first_name} {self.patient.surname}: Discharge"
