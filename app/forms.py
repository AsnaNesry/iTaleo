from django import forms
import datetime


class JobDetailsForm(forms.Form):
    job_code = forms.CharField(max_length=100)
    job_title = forms.CharField(max_length=100)
    job_description = forms.CharField(max_length=1000)
    job_type = forms.CharField(max_length=100)
    job_categories = forms.CharField(max_length=100)
    offered_salary = forms.DecimalField(max_digits=6, decimal_places=2)
    career_level = forms.CharField(max_length=100)
    required_experience = forms.IntegerField
    required_gender = forms.CharField(max_length=10, required=False)
    industry = forms.CharField(max_length=100)
    qualification = forms.CharField(max_length=100)
    application_deadline = forms.DateField(default=datetime.date.today, required=False)
    key_skills = forms.CharField(max_length=500)

