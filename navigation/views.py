from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'navigation/home.html')


@login_required
def options(request):
    return render(request, 'navigation/options.html')
