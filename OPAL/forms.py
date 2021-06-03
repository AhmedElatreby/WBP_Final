from django.forms import ModelForm
from django import forms
from . models import (Team, Patient, IndirectInput, Therapy,
                      Therapist, DirectInput)


class PatientForm(ModelForm):
    date_of_birth = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'),
                                    input_formats=('%d/%m/%Y',))

    class Meta:
        model = Patient
        fields = "__all__"


class TherapyForm(ModelForm):
    class Meta:
        model = Therapy
        fields = "__all__"
        exclude = ["patient"]


class TherapistForm(ModelForm):
    class Meta:
        model = Therapist
        fields = "__all__"


class DirectInputForm(ModelForm):
    class Meta:
        model = DirectInput
        fields = "__all__"


class IndirectInputForm(ModelForm):
    class Meta:
        model = IndirectInput
        fields = "__all__"


class AssignedTeamForm(ModelForm):
    class Meta:
        model = Team
        fields = "__all__"
