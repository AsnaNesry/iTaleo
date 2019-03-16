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
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
