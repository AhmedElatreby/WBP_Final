from django.shortcuts import render
from ..forms import DirectInputForm, IndirectInputForm
from django.shortcuts import redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from ..models import Patient


# This view creates a direct input type for a therapy.
@staff_member_required(login_url="/login/")
def direct_input_create(request, id):
    if request.method == "POST":
        form = DirectInputForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Direct Input successfully created.')
            return redirect("OPAL:therapy_create", id=id)
    else:
        form = DirectInputForm()
    return render(request, "OPAL/therapy/inputs/direct/create.html", {"form": form, "patient": Patient.objects.get(id=id)})


# This view creates a indirect input type for a therapy.
@staff_member_required(login_url="/login/")
def indirect_input_create(request, id):
    if request.method == "POST":
        form = IndirectInputForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Indirect Input successfully created.')
            return redirect("OPAL:therapy_create", id=id)
    else:
        form = IndirectInputForm()
    return render(request, "OPAL/therapy/inputs/indirect/create.html", {"form": form, "patient": Patient.objects.get(id=id)})
