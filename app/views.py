from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from django.contrib.auth import logout
# Create your views here.


def employer_login(request):
    msg = []
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if is_member(user) and user.is_active:
                login(request, user)
                return redirect('employer_dashboard')
            else:
                msg.append("Invalid Login")
        else:
            msg.append("Invalid Login")
    return render(request, 'employer_login.html', {'errors': msg})


def is_member(user):
    return user.groups.filter(name='HrGroup').exists()


@login_required
def show_employer_dashboard(request):
    return render(request, 'employer_manage_jobs.html')


def employer_logout(request):
    logout(request)
    return render(request, 'employer_login.html')
