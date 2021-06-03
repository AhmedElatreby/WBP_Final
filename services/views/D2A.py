from django.shortcuts import render
from ..forms import D2AForm
from django.shortcuts import redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from OPAL.models import Patient
from ..models import D2A


# Creates a D2A object and stores it in the database
@staff_member_required(login_url="/login/")
def D2A_create(request, id):
    patient = Patient.objects.get(id=id)
    if request.method == "POST":
        form = D2AForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.patient = patient
            task = form.save()
            messages.success(request, 'D2A successfully created.')
            return redirect("services:D2A_list", patient.id)
    else:
        form = D2AForm()
    return render(request, "services/D2A/create.html", {"form": form, "patient": patient})


# This view edits a D2A object, populates the form with
# existing data.
@staff_member_required(login_url="/login/")
def D2A_edit(request, id):
    d2a = D2A.objects.get(id=id)
    if request.method == "POST":
        form = D2AForm(request.POST, instance=d2a)
        if form.is_valid():
            form.save()
            messages.success(request, 'D2A successfully updated.')
            return redirect("services:D2A_list", id=d2a.patient.id)
    else:
        data = {"therapist_completing_D2A": d2a.therapist_completing_D2A, "D2A_completion_date": d2a.D2A_completion_date}
        form = D2AForm(initial=data)
    return render(request, "services/D2A/edit.html", {"form": form, "D2A": d2a})


# Gets a list of D2A's for a given patient
@login_required
def D2A_list(request, id):
    patient = Patient.objects.get(id=id)
    D2As = D2A.objects.filter(patient=patient).order_by("-updated_at", "-created_at")
    return render(request, "services/D2A/list.html", {"D2As": D2As, "patient": patient})


# Deletes a D2A from the database
@staff_member_required(login_url="/login/")
def D2A_delete(request, id):
    d2a = D2A.objects.get(id=id)
    d2a.delete()
    messages.error(request, 'D2A successfully deleted.')
    return redirect("OPAL:patient_single", d2a.patient.id)
