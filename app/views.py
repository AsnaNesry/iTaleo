from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from django.contrib.auth import logout
from .models import JobDetailsForm
from .models import JobDetails
from django.http import JsonResponse


# Create your views here.


def employer_login(request):
    msg = []
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if is_HR(user) and user.is_active:
                login(request, user)
                return redirect('employer_dashboard')
            else:
                msg.append("Invalid Login")
        else:
            msg.append("Invalid Login")
    return render(request, 'employer_login.html', {'errors': msg})


def is_HR(user):
    return user.groups.filter(name='HrGroup').exists()


@login_required
def show_employer_dashboard(request):
    all_jobs = JobDetails.objects.all().order_by('-creation_date')
    return_obj = {
        "jobDetails": all_jobs
    }
    return render(request, 'employer_manage_jobs.html', return_obj)


def employer_logout(request):
    logout(request)
    return render(request, 'employer_login.html')


def save_job_details(request):
    if request.method == 'POST':
        form = JobDetailsForm(request.POST)
        user = request.user
        if form.is_valid():
            job_details = form.save(commit=False)
            job_details.created_by = user
            job_details.save()
            return redirect('employer_dashboard')
    else:
        form = JobDetailsForm()

    return redirect(request, '/employer_post_new.html')


def candidate_signup(request):
    msg = []
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid:
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('candidate_dashboard')
        else:
            msg.append("Invalid Registration")
    else:
        msg.append("Invalid Registration")

    return redirect(request, '/')


def candidate_login(request):
    msg = []
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if not is_HR(user) and user.is_active:
                login(request, user)
                return redirect('candidate_dashboard')
            else:
                msg.append("Invalid Login")
        else:
            msg.append("Invalid Login")
    return render(request, 'index.html', {'errors': msg})


def candidate_dashboard(request):
    return render(request, 'candidates_dashboard.html')


def candidate_profile_basic(request):
    return render(request, 'candidates_profile_basic.html')


def candidate_profile_career(request):
    return render(request, 'candidates_profile_career.html')


def add_education(request):
    education_details = []
    added_detail = EducationDetails(request.POST.get('qualification'), request.POST.get('specialization'),
                                    request.POST.get('from_date'),
                                    request.POST.get('to_date'), request.POST.get('percentage'),
                                    request.POST.get('institution'))
    if 'education_details' in request.session:
        education_details = request.session['education_details']
    else:
        print("Nothing")
    education_details.append(added_detail)
    request.session['education_details'] = education_details
    return render(request, 'candidates_profile_career.html', {'education_details': education_details})


class EducationDetails(object):
    def __init__(self, qualification, specialization, from_date, to_date, percentage, institution):
        self.qualification = qualification
        self.specialization = specialization
        self.from_date = from_date
        self.to_date = to_date
        self.percentage = percentage
        self.institution = institution
