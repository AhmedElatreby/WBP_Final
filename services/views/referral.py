from django.shortcuts import render
from ..forms import ReferralForm
from django.shortcuts import redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from OPAL.models import Patient
from ..models import Referral


# This view creates a referral object and saves it to the
# database.
@staff_member_required(login_url="/login/")
def referral_create(request, id):
    patient = Patient.objects.get(id=id)
    if request.method == "POST":
        form = ReferralForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.patient = patient
            task = form.save()
            messages.success(request, 'Referral successfully created.')
            return redirect("services:referral_list", patient.id)
    else:
        form = ReferralForm()
    return render(request, "services/referral/create.html", {"form": form, "patient": patient})


# This view edits a referral object and populates the form with
# existing data
@staff_member_required(login_url="/login/")
def referral_edit(request, id):
    referral = Referral.objects.get(id=id)
    if request.method == "POST":
        form = ReferralForm(request.POST, instance=referral)
        if form.is_valid():
            form.save()
            messages.success(request, 'Referral successfully updated.')
            return redirect("services:referral_list", id=referral.patient.id)
    else:
        data = {"type_of_referral": referral.type_of_referral, "therapist_referring": referral.therapist_referring,
                "referral_date": referral.referral_date, "initial_contact_date": referral.initial_contact_date}
        form = ReferralForm(initial=data)
    return render(request, "services/referral/edit.html", {"form": form, "referral": referral})


# Gets all referrals for a given patient
@login_required
def referral_list(request, id):
    patient = Patient.objects.get(id=id)
    referrals = Referral.objects.filter(patient=patient).order_by('-created_at')
    return render(request, "services/referral/list.html", {"referrals": referrals, "patient": patient})


# Deletes a referral from a given patient
@staff_member_required(login_url="/login/")
def referral_delete(request, id):
    referral = Referral.objects.get(id=id)
    referral.delete()
    messages.error(request, 'Referral successfully deleted.')
    return redirect("OPAL:patient_single", id=referral.patient.id)
