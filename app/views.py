from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from django.contrib.auth import logout
from .models import JobDetailsForm
from .models import JobDetails
from .models import EducationDetailsForm
from .models import WorkExperienceForm
from .models import SkillSetForm


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
    errors = []
    if request.method == 'POST':
        form = JobDetailsForm(request.POST)
        user = request.user
        if form.is_valid():
            job_details = form.save(commit=False)
            job_details.created_by = user
            job_details.save()
            return redirect('employer_dashboard')
        else:
            print("Err")
    return render(request, 'employer_post_new.html', {'errors': errors})


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
    education_return_list = []
    work_experience_return_list = []
    skill_set_return_list = []
    if 'education_details' in request.session:
        education_details = request.session['education_details']
        populate_education_return_list(education_details, education_return_list)
    if 'work_experience_details' in request.session:
        work_experience_details = request.session['work_experience_details']
        populate_work_experience_return_list(work_experience_details, work_experience_return_list)
    if 'skill_details' in request.session:
        skill_details = request.session['skill_details']
        populate_skill_set(skill_details, skill_set_return_list)
    return render(request, 'candidates_profile_career.html', {'education_return_list': education_return_list,
                                                              'work_experience_return_list': work_experience_return_list,
                                                              'skill_set_return_list': skill_set_return_list})


def add_education(request):
    education_details = []
    if request.method == 'POST':
        form = EducationDetailsForm(request.POST)
        if form.is_valid:
            qualification = request.POST.get('qualification')
            specialization = request.POST.get('specialization')
            from_date = request.POST.get('from_date')
            to_date = request.POST.get('to_date')
            percentage = request.POST.get('percentage')
            institution = request.POST.get('institution')
            added_detail = {'qualification': qualification, 'specialization': specialization,
                            'from_date': from_date,
                            'to_date': to_date, 'percentage': percentage, 'institution': institution}
            if 'education_details' in request.session:
                education_details = request.session['education_details']
            education_details.append(added_detail)
            request.session['education_details'] = education_details
    return redirect('candidate_profile_career')


def populate_education_return_list(education_details, return_list):
    if education_details is not None:
        for num, element in enumerate(education_details):
            qualification = element['qualification']
            specialization = element['specialization']
            from_date = element['from_date']
            to_date = element['to_date']
            percentage = element['percentage']
            institution = element['institution']
            current_element = {'qualification': qualification, 'specialization': specialization,
                               'from_date': from_date,
                               'to_date': to_date, 'percentage': percentage, 'institution': institution}
            return_list.append(current_element)


def add_work_experience(request):
    work_experience_details = []
    if request.method == 'POST':
        form = WorkExperienceForm(request.POST)
        if form.is_valid:
            job_title = request.POST.get('job_title')
            from_date = request.POST.get('from_date')
            to_date = request.POST.get('to_date')
            is_present_job = request.POST.get('is_present_job')
            company_name = request.POST.get('company_name')
            project_details = request.POST.get('project_details')
            added_detail = {'job_title': job_title, 'is_present_job': is_present_job,
                            'from_date': from_date,
                            'to_date': to_date, 'company_name': company_name, 'project_details': project_details}
            if 'work_experience_details' in request.session:
                work_experience_details = request.session['work_experience_details']
            work_experience_details.append(added_detail)
            request.session['work_experience_details'] = work_experience_details
    return redirect('candidate_profile_career')


def populate_work_experience_return_list(work_experience_details, return_list):
    if work_experience_details is not None:
        for num, element in enumerate(work_experience_details):
            job_title = element['job_title']
            is_present_job = element['is_present_job']
            from_date = element['from_date']
            to_date = element['to_date']
            company_name = element['company_name']
            project_details = element['project_details']
            current_element = {'job_title': job_title, 'is_present_job': is_present_job,
                               'from_date': from_date,
                               'to_date': to_date, 'project_details': project_details,
                               'company_name': company_name}
            return_list.append(current_element)


def add_skill_set(request):
    skill_details = []
    if request.method == 'POST':
        form = SkillSetForm(request.POST)
        if form.is_valid:
            skill_name = request.POST.get('skill_name')
            skill_percentage = request.POST.get('skill_percentage')
            added_detail = {'skill_name': skill_name, 'skill_percentage': skill_percentage}
            if 'skill_details' in request.session:
                skill_details = request.session['skill_details']
            skill_details.append(added_detail)
            request.session['skill_details'] = skill_details
    return redirect('candidate_profile_career')


def populate_skill_set(skill_details, return_list):
    if skill_details is not None:
        for num, element in enumerate(skill_details):
            skill_name = element['skill_name']
            skill_percentage = element['skill_percentage']
            current_element = {'skill_name': skill_name, 'skill_percentage': skill_percentage}
            return_list.append(current_element)


def candidate_logout(request):
    logout(request)
    return redirect('')

