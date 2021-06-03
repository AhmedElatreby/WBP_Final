from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from OPAL.models import Patient


# Returns a view that shows all options to add information to a given patient
@staff_member_required(login_url="/login/")
def add_service(request, id):
    patient = Patient.objects.get(id=id)
    return render(request, "services/add_service.html", {"patient": patient})


# Returns a view that shows all options to view information about a given patient
@login_required
def view_services(request, id):
    patient = Patient.objects.get(id=id)
    return render(request, "services/view_services.html", {"patient": patient})
