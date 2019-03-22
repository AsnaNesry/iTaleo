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
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=100, default='Active')
    total_applied = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    creation_date = models.DateTimeField(default=datetime.now)


def __str__(self):
    return self.name


class JobDetailsForm(ModelForm):
    class Meta:
        model = JobDetails
        fields = ['job_code', 'job_title', 'job_description', 'job_type', 'job_categories', 'minimum_salary',
                  'maximum_salary',
                  'career_level', 'minimum_experience', 'maximum_experience', 'required_gender', 'industry',
                  'qualification',
                  'application_deadline', 'key_skills', 'country', 'city', 'status']
