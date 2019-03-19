from django.db import models
import datetime
from django.forms import ModelForm


class JobDetails(models.Model):
    job_code = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100)
    job_description = models.CharField(max_length=1000)
    job_type = models.CharField(max_length=100)
    job_categories = models.CharField(max_length=100)
    offered_salary = models.DecimalField(max_digits=6, decimal_places=2)
    career_level = models.CharField(max_length=100)
    required_experience = models.IntegerField(default=0)
    required_gender = models.CharField(max_length=10)
    industry = models.CharField(max_length=100)
    qualification = models.CharField(max_length=100)
    application_deadline = models.DateField(default=datetime.date.today)
    key_skills = models.CharField(max_length=500)
    created_by = models.CharField(max_length=100)
    creation_date = models.DateField(default=datetime.date.today)


def __str__(self):
    return self.name


class JobDetailsForm(ModelForm):
    class Meta:
        model = JobDetails
        fields = ['job_code', 'job_title', 'job_description', 'job_type', 'job_categories', 'offered_salary',
                  'career_level', 'required_experience', 'required_gender', 'industry', 'qualification',
                  'application_deadline', 'key_skills']
