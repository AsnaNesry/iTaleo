from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .models import JobDetailsForm
from .models import JobDetails
from .models import EducationDetailsForm
from .models import WorkExperienceForm
from .models import SkillSetForm
from .models import CandidateProfileForm
from .models import CandidateProfile
from .models import EducationDetails
from .models import WorkExperience
from .models import SkillSet
from .models import JobApplication
import pandas as pd
import pickle


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
            user_name_obj = user.username
            CandidateProfile.objects.create(user_id=user_name_obj)
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
    user_id = request.user.username
    basic_details_db = CandidateProfile.objects.all().filter(user_id=user_id)
    if basic_details_db is not None:
        return_object = []
        for element in basic_details_db:
            return_object = {'full_name': element.full_name, 'job_title': element.job_title, 'age': element.age,
                             'experience': element.experience, 'current_salary': element.current_salary,
                             'expected_salary': element.expected_salary,
                             'highest_education': element.highest_education,
                             'profile_description': element.profile_description, 'phone_number': element.phone_number,
                             'email': element.email, 'website': element.website, 'country': element.country,
                             'city': element.city, 'current_company': element.current_company}
        return render(request, 'candidates_profile_basic.html', {'profile_details': return_object})
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


def delete_skill_set(request, value):
    if 'skill_details' in request.session:
        skill_details = request.session['skill_details']
        skill_details[:] = [d for d in skill_details if d.get('skill_name') != value]
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
    return redirect('/')


def save_candidate_basic_details(request):
    if request.method == 'POST':
        form = CandidateProfileForm(request.POST)
        if form.is_valid:
            user_id = request.user.username
            full_name = request.POST.get('full_name')
            job_title = request.POST.get('job_title')
            age = request.POST.get('age')
            experience = request.POST.get('experience')
            current_salary = request.POST.get('current_salary')
            expected_salary = request.POST.get('expected_salary')
            highest_education = request.POST.get('highest_education')
            profile_description = request.POST.get('profile_description')
            phone_number = request.POST.get('phone_number')
            email = request.POST.get('email')
            website = request.POST.get('website')
            country = request.POST.get('country')
            city = request.POST.get('city')
            current_company = request.POST.get('current_company')
            CandidateProfile.objects.filter(user_id=user_id).update(full_name=full_name, job_title=job_title, age=age,
                                                                    experience=experience,
                                                                    current_salary=current_salary,
                                                                    expected_salary=expected_salary,
                                                                    highest_education=highest_education,
                                                                    profile_description=profile_description,
                                                                    phone_number=phone_number, email=email,
                                                                    website=website, country=country, city=city,
                                                                    current_company=current_company)
    return redirect('/candidate_dashboard')


def save_career_details(request):
    user_id = request.user.username
    if 'education_details' in request.session:
        education_details = request.session['education_details']
        for education in education_details:
            EducationDetails.objects.update_or_create(user_id=user_id, qualification=education['qualification'],
                                                      defaults={'specialization': education['specialization'],
                                                                'from_date': education['from_date'],
                                                                'to_date': education['to_date'],
                                                                'percentage': education['percentage'],
                                                                'institution': education['institution'], })
    if 'work_experience_details' in request.session:
        work_experience_details = request.session['work_experience_details']
        for work_experience in work_experience_details:
            WorkExperience.objects.update_or_create(user_id=user_id, job_title=work_experience['job_title'],
                                                    defaults={'is_present_job': work_experience['is_present_job'],
                                                              'from_date': work_experience['from_date'],
                                                              'to_date': work_experience['to_date'],
                                                              'company_name': work_experience['company_name'],
                                                              'project_details': work_experience['project_details'], })
    if 'skill_details' in request.session:
        skill_set_details = request.session['skill_details']
        for skill_set in skill_set_details:
            SkillSet.objects.update_or_create(user_id=user_id, skill_name=skill_set['skill_name'],
                                              defaults={'skill_percentage': skill_set['skill_percentage'],
                                                        })
    return redirect('/candidate_dashboard')


def display_experience_and_career_details(request):
    user_id = request.user.username
    education_details = EducationDetails.objects.all().filter(user_id=user_id)
    career_details = WorkExperience.objects.all().filter(user_id=user_id)
    skill_details = SkillSet.objects.all().filter(user_id=user_id)
    if education_details is not None:
        education_details_list = []
        for element in education_details:
            current_element = {'qualification': element.qualification, 'specialization': element.specialization,
                               'from_date': str(element.from_date), 'to_date': str(element.to_date),
                               'percentage': element.percentage, 'institution': element.institution}
            education_details_list.append(current_element)
        request.session['education_details'] = education_details_list
    if career_details is not None:
        career_details_list = []
        for element in career_details:
            current_element = {'job_title': element.job_title, 'is_present_job': element.is_present_job,
                               'from_date': str(element.from_date), 'to_date': str(element.to_date),
                               'company_name': element.company_name, 'project_details': element.project_details}
            career_details_list.append(current_element)
        request.session['work_experience_details'] = career_details_list
    if skill_details is not None:
        skill_details_list = []
        for element in skill_details:
            current_element = {'skill_name': element.skill_name, 'skill_percentage': element.skill_percentage}
            skill_details_list.append(current_element)
        request.session['skill_details'] = skill_details_list
    return redirect('candidate_profile_career')


def search_job(request):
    user_id = request.user.username
    all_jobs = JobDetails.objects.all()
    applied_jobs = JobApplication.objects.all().filter(user_id=user_id)
    applied_job_list = []
    for job in applied_jobs:
        applied_job_list.append(job.job_code)

    job_list = []
    for element in all_jobs:
        job_code = element.job_code
        job_title = element.job_title
        key_skills = element.key_skills.replace(',', '  ')
        city = element.city
        country = element.country
        if job_code in applied_job_list:
            apply_status = 'APPLIED'
        else:
            apply_status = 'APPLY NOW'
        current_element = {'job_code': job_code, 'job_title': job_title, 'key_skills': key_skills, 'city': city,
                           'country': country, 'apply_status': apply_status, }
        job_list.append(current_element)
    return render(request, 'job_search.html', {'job_list': job_list})


def apply_job(request, value):
    user_id = request.user.username
    job_code = value
    JobApplication.objects.create(user_id=user_id, job_code=job_code)
    return redirect('search_job')


def view_job(request, value):
    user_id = request.user.username
    job_code = value
    job_details = JobDetails.objects.all().filter(job_code=job_code)
    applied_jobs = JobApplication.objects.all().filter(user_id=user_id)
    applied_job_list = []
    for job in applied_jobs:
        applied_job_list.append(job.job_code)
    job_detail = {}
    skill_description_list = []
    education_description_list = []
    html_page = 'job_single_view.html'
    if job_details:
        for job in job_details:
            job_code = job.job_code
            job_title = job.job_title
            job_description = job.job_description
            job_type = job.job_type
            job_categories = job.job_categories
            minimum_salary = job.minimum_salary
            maximum_salary = job.maximum_salary
            career_level = job.career_level
            minimum_experience = job.minimum_experience
            maximum_experience = job.maximum_experience
            required_gender = job.required_gender
            industry = job.industry
            qualification = job.qualification
            application_deadline = job.application_deadline
            key_skills = job.key_skills
            secondary_skills = job.secondary_skills
            country = job.country
            city = job.city
            status = job.status
            creation_date = job.creation_date
            if is_HR(request.user):
                html_page = 'employer_job_single_view.html'
                job_applied = 'employer'
            elif job_code in applied_job_list:
                job_applied = 'yes'
            else:
                job_applied = 'no'
            education_detail_desc = job.education_detail_desc
            skill_detailed_desc = job.skill_detailed_desc
            if skill_detailed_desc is not None:
                skill_description_list = skill_detailed_desc.split('• ')
                del skill_description_list[0]
            if education_detail_desc is not None:
                education_description_list = education_detail_desc.split('• ')
                del education_description_list[0]
            job_detail = {'job_code': job_code, 'job_title': job_title, 'job_title': job_title,
                          'job_description': job_description,
                          'job_type': job_type, 'job_categories': job_categories, 'minimum_salary': minimum_salary,
                          'maximum_salary': maximum_salary,
                          'career_level': career_level, 'minimum_experience': minimum_experience,
                          'maximum_experience': maximum_experience, 'required_gender': required_gender,
                          'industry': industry, 'qualification': qualification,
                          'application_deadline': application_deadline, 'key_skills': key_skills,
                          'secondary_skills': secondary_skills,
                          'country': country, 'city': city, 'status': status, 'creation_date': creation_date,
                          'job_applied': job_applied}
    return render(request, html_page,
                  {'job_detail': job_detail, 'skill_description_list': skill_description_list,
                   'education_description_list': education_description_list})


def view_applicants(request, value):
    job_code = value
    applicant_list = JobApplication.objects.all().filter(job_code=job_code)
    candidate_list = []
    rejected_list = []
    candidate_id_list = []
    if applicant_list:
        for applicant in applicant_list:
            candidate_id_list.append(applicant.user_id)
        ranked_candidate_name_list, rejected_candidate_name_list = rank_profiles(candidate_id_list, job_code)

        for candidate_name in ranked_candidate_name_list:
            candidate_db = CandidateProfile.objects.all().filter(user_id=candidate_name)
            for candidate in candidate_db:
                current_element = {'user_id': candidate.user_id, 'full_name': candidate.full_name,
                                   'job_title': candidate.job_title, 'current_company': candidate.current_company,
                                   'city': candidate.city, 'country': candidate.country}
                candidate_list.append(current_element)

        for candidate_name in rejected_candidate_name_list:
            candidate_db = CandidateProfile.objects.all().filter(user_id=candidate_name)
            for candidate in candidate_db:
                current_element = {'user_id': candidate.user_id, 'full_name': candidate.full_name,
                                   'job_title': candidate.job_title, 'current_company': candidate.current_company,
                                   'city': candidate.city, 'country': candidate.country}
                rejected_list.append(current_element)
    return render(request, 'candidates_list.html', {'candidate_list': candidate_list, 'rejected_list': rejected_list})


def view_profile(request, value):
    user_id = value
    candidate_details_obj = {}
    candidate_education_list = []
    candidate_work_experience_list = []
    candidate_skill_set_list = []
    candidate_details = CandidateProfile.objects.all().filter(user_id=user_id)
    candidate_education = EducationDetails.objects.all().filter(user_id=user_id)
    candidate_work_experience = WorkExperience.objects.all().filter(user_id=user_id)
    candidate_skill_set = SkillSet.objects.all().filter(user_id=user_id)
    if candidate_details:
        for element in candidate_details:
            candidate_details_obj = {'full_name': element.full_name, 'job_title': element.job_title, 'age': element.age,
                                     'experience': element.experience, 'current_salary': element.current_salary,
                                     'expected_salary': element.expected_salary,
                                     'highest_education': element.highest_education,
                                     'profile_description': element.profile_description,
                                     'phone_number': element.phone_number,
                                     'email': element.email, 'website': element.website, 'country': element.country,
                                     'city': element.city, 'current_company': element.current_company}
    if candidate_education:
        for element in candidate_education:
            current_element = {'qualification': element.qualification, 'specialization': element.specialization,
                               'from_date': element.from_date,
                               'to_date': element.to_date, 'percentage': element.percentage,
                               'institution': element.institution}
            candidate_education_list.append(current_element)
    if candidate_work_experience:
        for element in candidate_work_experience:
            current_element = {'job_title': element.job_title, 'is_present_job': element.is_present_job,
                               'from_date': element.from_date,
                               'to_date': element.to_date, 'project_details': element.project_details,
                               'company_name': element.company_name}
            candidate_work_experience_list.append(current_element)
    if candidate_skill_set:
        display_skills = []
        count = 0
        for element in candidate_skill_set:
            current_element = {'skill_name': element.skill_name, 'skill_percentage': element.skill_percentage}
            candidate_skill_set_list.append(current_element)
            if count < 3:
                display_skills.append(element.skill_name)
                count = count + 1
    html_page = ''
    if is_HR(request.user):
        html_page = 'employer_candidates_single.html'
    else:
        html_page = 'candidates_profile_view.html'
    return render(request, html_page,
                  {'candidate_details_obj': candidate_details_obj, 'candidate_education_list': candidate_education_list,
                   'candidate_work_experience_list': candidate_work_experience_list,
                   'candidate_skill_set_list': candidate_skill_set_list, 'display_skills': display_skills})


def rank_profiles(applied_candidate_list, job_code):
    job_details = JobDetails.objects.all().filter(job_code=job_code)
    job_primary_skills = []
    job_secondary_skills = []
    primary_skill_frame = []
    secondary_skill_frame = []
    user_frame = []
    education_frame = []
    experience_frame = []
    salary_frame = []
    for job in job_details:
        job_primary_skills = job.key_skills.split(',')
        job_secondary_skills = job.secondary_skills.split(',')
    for candidate in applied_candidate_list:
        skill_sets = SkillSet.objects.all().filter(user_id=candidate)
        primary_skill_total = 0
        secondary_skill_total = 0
        for skill in skill_sets:
            if skill.skill_name in job_primary_skills:
                primary_skill_total = primary_skill_total + skill.skill_percentage
            elif skill.skill_name in job_secondary_skills:
                secondary_skill_total = secondary_skill_total + skill.skill_percentage
        candidate_profile = CandidateProfile.objects.filter(user_id=candidate)
        for profile in candidate_profile:
            experience_frame.append(profile.experience)
            salary_frame.append(profile.expected_salary)
        education_count = EducationDetails.objects.filter(user_id=candidate).count()
        education_frame.append(education_count)
        user_frame.append(candidate)
        primary_skill_frame.append(primary_skill_total)
        secondary_skill_frame.append(secondary_skill_total)

    my_dict = {'salaries': salary_frame,
               'experience': experience_frame,
               'primary_skill_score': primary_skill_frame,
               'secondary_skill_score': secondary_skill_frame,
               'education': education_frame}
    input_data_frame = pd.DataFrame(my_dict)
    loaded_model = pickle.load(open(job_code+'.sav', 'rb'))
    prediction = loaded_model.predict(input_data_frame)
    probability = loaded_model.predict_proba(input_data_frame, check_input=True)

    all_detail_list = []
    for index, user_name in enumerate(user_frame):
        detail_dict = {'user_id': user_name, 'is_selected': prediction[index], 'score': probability[index][1]}
        all_detail_list.append(detail_dict)
    sorted_list = sorted(all_detail_list, key=lambda k: k['score'], reverse=True)
    print("Dictionary: ", sorted_list)
    filtered_list = list(filter(lambda d: d['is_selected'] == 1, sorted_list))
    rejected_list = list(filter(lambda d: d['is_selected'] == 0, sorted_list))
    selected_user_list = list(map(lambda d: d['user_id'], filtered_list))
    rejected_user_list = list(map(lambda d: d['user_id'], rejected_list))
    return selected_user_list, rejected_user_list


def view_candidate_profile(request):
    user_id = request.user.username
