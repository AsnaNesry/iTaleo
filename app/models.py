from django.db import models
from datetime import datetime
from django.forms import ModelForm
from django.contrib.auth.models import User


class JobDetails(models.Model):
    job_code = models.CharField(max_length=100, primary_key=True)
    job_title = models.CharField(max_length=100)
    job_description = models.CharField(max_length=1000)
    job_type = models.CharField(max_length=100)
    job_categories = models.CharField(max_length=100)
    minimum_salary = models.DecimalField(max_digits=14, decimal_places=2)
    maximum_salary = models.DecimalField(max_digits=14, decimal_places=2)
    career_level = models.CharField(max_length=100)
    minimum_experience = models.IntegerField(default=0)
    maximum_experience = models.IntegerField(default=0)
    required_gender = models.CharField(max_length=10)
    industry = models.CharField(max_length=100)
    qualification = models.CharField(max_length=100)
    application_deadline = models.DateField(blank=True)
    key_skills = models.CharField(max_length=500)
    secondary_skills = models.CharField(max_length=500, null=True)
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=100, default='Active')
    total_applied = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    creation_date = models.DateTimeField(default=datetime.now)
    education_detail_desc = models.CharField(max_length=1000, blank=True, null=True)
    skill_detailed_desc = models.CharField(max_length=1000, blank=True, null=True)


class CandidateProfile(models.Model):
    user_id = models.CharField(max_length=50, primary_key=True, default="abc")
    full_name = models.CharField(max_length=200, blank=True, null=True)
    job_title = models.CharField(max_length=200, blank=True, null=True)
    age = models.IntegerField(default=0, blank=True, null=True)
    experience = models.IntegerField(default=0, blank=True, null=True)
    current_salary = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    expected_salary = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    highest_education = models.CharField(max_length=50, blank=True, null=True)
    profile_description = models.CharField(max_length=1000, blank=True, null=True)
    phone_number = models.IntegerField(default=0, blank=True, null=True)
    email = models.EmailField(max_length=30, blank=True, null=True)
    website = models.CharField(max_length=30, blank=True, null=True)
    country = models.CharField(max_length=30, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    current_company = models.CharField(max_length=100, null=True)


def __str__(self):
    return self.name


class JobDetailsForm(ModelForm):
    class Meta:
        model = JobDetails
        fields = ['job_code', 'job_title', 'job_description', 'job_type', 'job_categories', 'minimum_salary',
                  'maximum_salary',
                  'career_level', 'minimum_experience', 'maximum_experience', 'required_gender', 'industry',
                  'qualification',
                  'application_deadline', 'key_skills', 'country', 'city', 'secondary_skills', 'education_detail_desc',
                  'skill_detailed_desc']


class CandidateProfileForm(ModelForm):
    class Meta:
        model = CandidateProfile
        fields = ['full_name', 'job_title', 'age', 'experience', 'current_salary', 'expected_salary',
                  'highest_education', 'profile_description', 'phone_number', 'email', 'website', 'country', 'city',
                  'current_company']


class EducationDetails(models.Model):
    class Meta:
        unique_together = (('user_id', 'qualification'),)

    user_id = models.CharField(max_length=50, default="abc")
    qualification = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    from_date = models.DateField()
    to_date = models.DateField()
    percentage = models.IntegerField(default=0)
    institution = models.CharField(max_length=100)


class EducationDetailsForm(ModelForm):
    class Meta:
        model = EducationDetails
        fields = ['qualification', 'specialization', 'from_date', 'to_date', 'percentage', 'institution']


class WorkExperience(models.Model):
    class Meta:
        unique_together = (('user_id', 'job_title'),)

    user_id = models.CharField(max_length=50, default="abc")
    job_title = models.CharField(max_length=100)
    from_date = models.DateField()
    to_date = models.DateField()
    is_present_job = models.BooleanField(default=False, null=True)
    company_name = models.CharField(max_length=100)
    project_details = models.CharField(max_length=500)


class WorkExperienceForm(ModelForm):
    class Meta:
        model = WorkExperience
        fields = ['job_title', 'from_date', 'to_date', 'is_present_job', 'company_name', 'project_details']


class SkillSet(models.Model):
    class Meta:
        unique_together = (('user_id', 'skill_name'),)

    user_id = models.CharField(max_length=50, default="abc")
    skill_name = models.CharField(max_length=100)
    skill_percentage = models.IntegerField(default=0)


class SkillSetForm(ModelForm):
    class Meta:
        model = SkillSet
        fields = ['skill_name', 'skill_percentage']


class JobApplication(models.Model):
    class Meta:
        unique_together = (('user_id', 'job_code'))

    user_id = models.CharField(max_length=50)
    job_code = models.CharField(max_length=100)
