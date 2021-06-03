from django.shortcuts import render
from ..models import Therapy, Therapist
from ..forms import TherapistForm, AssignedTeamForm
from django.db.models import Avg, Q
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required


# The view returns a list of all therapists before searching.
@login_required
def therapist_list(request):
    return render(request, "OPAL/therapist/list.html")


# This view returns a single therapist object and the average
# direct and indirect times for therapies.
@login_required
def therapist_single(request, id):
    therapist = Therapist.objects.get(id=id)
    therapies = Therapy.objects.filter(therapist=id)
    indirect_average = therapies.aggregate(Avg('indirect_time'))
    direct_average = therapies.aggregate(Avg('direct_time'))
    return render(request, "OPAL/therapist/single.html", {"therapist": therapist, "therapies": therapies, "direct_average": direct_average["direct_time__avg"],
                                                          "indirect_average": indirect_average["indirect_time__avg"]})


# This view creates a therapist object and saves it to the
# database.
@staff_member_required(login_url="/login/")
def therapist_create(request):
    if request.method == "POST":
        form = TherapistForm(request.POST)
        if form.is_valid():
            task = form.save()
            messages.success(request, 'Therapist successfully created.')
            return redirect("OPAL:therapist_single", id=task.id)
    else:
        form = TherapistForm()
    return render(request, "OPAL/therapist/create.html", {"form": form})


# This view creates an assigned team for a therapist as a foreign
# key to be referenced
@staff_member_required(login_url="/login/")
def assigned_team_create(request):
    if request.method == "POST":
        form = AssignedTeamForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Assigned Team successfully created.')
            return redirect("OPAL:therapist_create")
    else:
        form = AssignedTeamForm()
    return render(request, "OPAL/therapist/assigned_team/create.html", {"form": form})


# This view edits a therapist object and populates the form with
# existing data
@staff_member_required(login_url="/login/")
def therapist_edit(request, id):
    therapist = Therapist.objects.get(id=id)
    if request.method == "POST":
        form = TherapistForm(request.POST, instance=therapist)
        if form.is_valid():
            form.save()
            messages.success(request, 'Therapist successfully updated.')
            return redirect("OPAL:therapist_single", id=id)
    else:
        data = {"first_name": therapist.first_name, "surname": therapist.surname,
                "Therapist_role": therapist.therapist_role, "band": therapist.band,
                "assigned_team": therapist.assigned_team}
        form = TherapistForm(instance=therapist, initial=data)
    return render(request, "OPAL/therapist/edit.html", {"form": form, "therapist": therapist})


# This view deletes the therapist object
@staff_member_required(login_url="/login/")
def therapist_delete(request, id):
    therapist = Therapist.objects.get(id=id)
    therapist.delete()
    messages.error(request, 'Therapist successfully deleted.')
    return redirect('OPAL:therapist_list')


# This view searches for a therapist object by the role, name, id and band
@login_required
def therapist_search(request):
    q = request.GET.get('q')
    messages = ""
    object_list = Therapist.objects.filter(
        Q(therapist_role__icontains=q) | Q(band__icontains=q) | Q(first_name__icontains=q) | Q(surname__icontains=q) | Q(id__icontains=q)
    )
    if len(object_list) == 0:
        messages = True
    return render(request, 'OPAL/therapist/list.html', {"therapists": object_list, "messages": messages})
