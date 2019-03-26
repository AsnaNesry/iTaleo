from django.conf.urls import url
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings
from . import views as app_views

urlpatterns = [
    url(r'^create_job/$', TemplateView.as_view(template_name='employer_post_new.html'), name='create_job'),
    url(r'^employer_login/$', TemplateView.as_view(template_name='employer_login.html'), name='employer_login'),
    url(r'^employer_logout/$', app_views.employer_logout, name='employer_logout'),
    url(r'^authenticate_employer/$', app_views.employer_login, name='authenticate_employer'),
    url(r'^employer_dashboard/$', app_views.show_employer_dashboard, name='employer_dashboard'),
    url(r'^save_job_details/$', app_views.save_job_details, name='save_job_details'),
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),
    url(r'^candidate_signup/$', app_views.candidate_signup, name='candidate_signup'),
    url(r'^candidate_login/$', app_views.candidate_login, name='candidate_login'),
    url(r'^candidate_dashboard/$', app_views.candidate_dashboard, name='candidate_dashboard'),
    url(r'^candidate_profile_basic/$', app_views.candidate_profile_basic, name='candidate_profile_basic'),
    url(r'^candidate_profile_career/$', app_views.candidate_profile_career, name='candidate_profile_career'),
    url(r'^add_education/$', app_views.add_education, name='add_education'),
    url(r'^add_work_experience/$', app_views.add_work_experience, name='add_work_experience'),
    url(r'^add_skill_set/$', app_views.add_skill_set, name='add_skill_set'),
    url(r'^candidate_logout/$', app_views.candidate_logout, name='candidate_logout'),
    url(r'^save_candidate_basic_details/$', app_views.save_candidate_basic_details,
        name='save_candidate_basic_details'),
    url(r'^save_career_details/$', app_views.save_career_details, name='save_career_details'),
    url(r'^display_experience_and_career_details/$', app_views.display_experience_and_career_details,
        name='display_experience_and_career_details'),
    url(r'^search_job/$', app_views.search_job, name='search_job'),
    url(r'^apply_job/(?P<value>\S+)/', app_views.apply_job, name='apply_job'),
    url(r'^view_job/(?P<value>\S+)/', app_views.view_job, name='view_job'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
