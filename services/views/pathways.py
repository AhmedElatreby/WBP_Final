from django.shortcuts import render
from ..forms import PathwayForm, ReferralSourceForm
from django.shortcuts import redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from OPAL.models import Patient
from ..models import Pathway


# This view creates a pathway object and saves it to the
# database.
@staff_member_required(login_url="/login/")
def pathway_create(request, id):
    patient = Patient.objects.get(id=id)
    if request.method == "POST":
        form = PathwayForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.patient = patient
            task = form.save()
            messages.success(request, 'Pathway successfully created.')
            return redirect("services:pathway_list", patient.id)
    else:
        form = PathwayForm()
    return render(request, "services/pathways/create.html", {"form": form, "patient": patient})


# This view edits a pathway object and populates the form with
# existing data
@staff_member_required(login_url="/login/")
def pathway_edit(request, id):
    pathway = Pathway.objects.get(id=id)
    if request.method == "POST":
        form = PathwayForm(request.POST, instance=pathway)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pathway successfully updated.')
            return redirect("services:pathway_list", id=pathway.patient.id)
    else:
        data = {"admission_date": pathway.admission_date, "meet_criteria_therapy": pathway.meet_criteria_therapy,
                "referral_source": pathway.referral_source, "front_door": pathway.front_door,
                "RAFT": pathway.RAFT, "CCMT": pathway.CCMT, "CCMT_date": pathway.CCMT_date,
                "admission_barthel": pathway.admission_barthel, "discharge_barthel": pathway.discharge_barthel}
        form = PathwayForm(initial=data)
    return render(request, "services/pathways/edit.html", {"form": form, "pathway": pathway})


# This view creates an referral source for a pathway as a foreign
# key to be referenced
@staff_member_required(login_url="/login/")
def referral_source_create(request, id):
    patient = Patient.objects.get(id=id)
    if request.method == "POST":
        form = ReferralSourceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Referral Source successfully created.')
            return redirect("services:pathway_create", id=patient.id)
    else:
        form = ReferralSourceForm()
    return render(request, "services/pathways/referral_source/create.html", {"form": form, "patient": patient})


# Gets all pathways for a given patient
@login_required
def pathway_list(request, id):
    patient = Patient.objects.get(id=id)
    pathways = Pathway.objects.filter(patient=patient).order_by('-created_at')
    return render(request, "services/pathways/list.html", {"pathways": pathways, "patient": patient})


# Deletes a pathway from a given patient
@staff_member_required(login_url="/login/")
def pathway_delete(request, id):
    pathway = Pathway.objects.get(id=id)
    pathway.delete()
    messages.error(request, 'Pathway successfully deleted.')
    return redirect("OPAL:patient_single", id=pathway.patient.id)
