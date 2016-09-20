"""
Definition of urls for square_connect.
"""

from datetime import datetime
from django.conf.urls import patterns, url
from app.forms import BootstrapAuthenticationForm
# My imports
import django.contrib.auth.views
from django.views.generic.base import RedirectView # For the favicon
from django.contrib import admin
from django.utils import timezone
# Uncomment the next lines to enable the admin:
from django.conf.urls import include
from django.contrib import admin
import app.views as app_views
import spoilage_report.views as spoilage_report_views
import mailer.views as mailer_views
admin.autodiscover()

urlpatterns = [
    url(r'^$', app_views.home, name='home'),
    url(r'^contact$', app_views.contact, name='contact'),
    url(r'^about', app_views.about, name='about'),
    url(r'^services', app_views.services, name='services'),
    url(r'^spoilage_report/$', spoilage_report_views.spoilage_report, name='spoilage_report'),
	url(r'^spoilage_report/([a-zA-Z]+)/([0-9]{4})/([0-9]{2})/([0-9]{2})/([0-9]{4})/([0-9]{2})/([0-9]{2})', spoilage_report_views.spoilage_report_date, name='spoilage_report_date'),
    url(r'^request_report', spoilage_report_views.request_report, name='request_report'),
    url(r'^mailer', mailer_views.mailer, name='mailer'),
	url(r'^login/$',
        django.contrib.auth.views.login,
        {
            'template_name': 'app/login.html',
            'authentication_form': BootstrapAuthenticationForm,
            'extra_context':
            {
                'title':'Log in',
                'year':timezone.now().year,
            }
        },
        name='login'),
    url(r'^logout$',
        django.contrib.auth.views.logout,
        {
            'next_page': '/',
        },
        name='logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', admin.site.urls),
    url(r'^mailinglists/$', mailer_views.mailer_admin, name='mailer_admin'),
    url(r'^favicon\.ico$', RedirectView.as_view(url='static/favicon.ico')),
]
