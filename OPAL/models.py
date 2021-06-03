from django.db import models
from django.urls import reverse


# Create the Assigned Team model in the database:
# Listed fields:
# - team_name: The name of the team
class Team(models.Model):
    team_name = models.CharField(max_length=50)

    def __str__(self):
        return self.team_name


# Create the therapist model in the database:
# Listed fields:
# - first_name, surname: The therapists name
# - therapist_role: The role of the therapist
# - band: The level of the therapist
# - assigned_team: The assigned team of the therapist
class Therapist(models.Model):

    # Enum for the therapist roles
    THERAPYASSISTANT = 'TA'
    OCCUPATIONTHERAPIST = 'OT'
    PHYSIOTHERAPY = 'PT'

    THERAPIST_ROLE_CHOICES = (
        (THERAPYASSISTANT, "Therapy Assistant"),
        (OCCUPATIONTHERAPIST, "Occupation Therapist"),
        (PHYSIOTHERAPY, "Physio Therapist"),
    )

    first_name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    therapist_role = models.CharField(
        max_length=2,
        choices=THERAPIST_ROLE_CHOICES,
        default=THERAPYASSISTANT
    )
    band = models.IntegerField(default=1)
    assigned_team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.surname}: {self.id}"

    def get_absolute_url(self):
        return reverse('OPAL:therapist_single', args=[str(self.id)])


# Create the patient model in the database:
# Listed fields:
# - hospital_number: The assigneed hospital number of a patient
# - first_name, surname: The patients name
# - date_of_birth: The date of birth of the patient
# - postcode: The postcode of the patient
# - locality: The locality (e.g. bournemouth) of the patient
class Patient(models.Model):
    hospital_number = models.CharField(max_length=15, unique=True)
    first_name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    postcode = models.CharField(max_length=8)
    locality = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.first_name} {self.surname}: {self.hospital_number}"

    def get_absolute_url(self):
        return reverse('OPAL:patient_single', args=[str(self.id)])


# Create the direct input model in the database:
# Listed fields:
# - title: The title of the direct input
class DirectInput(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


# Create the direct input model in the database:
# Listed fields:
# - title: The title of the indirect input
class IndirectInput(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


# Create the therapy model in the database:
# Listed fields:
# - patient: The patient recieving therapy
# - therapist: The therapist administering the therapy
# - rehab: Whether or not the therapy contains rehab
# - direct_input: The type of direct input
# - direct_time: The direct time this therapy took in minutes
# - indirect_input: The type of indirect input
# - indirect_time: The indirect time this therapy took in minutes
class Therapy(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE)
    rehab = models.BooleanField(default=False)
    direct_input = models.ForeignKey(DirectInput, blank=True, null=True,
                                     on_delete=models.SET_NULL)
    direct_time = models.IntegerField(null=True, blank=True)
    indirect_input = models.ForeignKey(IndirectInput, blank=True,
                                       null=True, on_delete=models.SET_NULL)
    indirect_time = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Therapies"

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('OPAL:therapy_single', args=[str(self.id)])
