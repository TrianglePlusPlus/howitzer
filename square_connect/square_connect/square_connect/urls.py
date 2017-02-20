"""
Definition of urls for square_connect.
"""

from datetime import datetime
from django.conf.urls import url
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
import mailer.views as mailer_views
import report.views as report_views
admin.autodiscover()

urlpatterns = [
    url(r'^$', app_views.home, name='home'),
    url(r'^contact$', app_views.contact, name='contact'),
    url(r'^about', app_views.about, name='about'),
    url(r'^services', app_views.services, name='services'),
    url(r'^mailer', mailer_views.mailer, name='mailer'),

    url(r'^report/$', report_views.report, name='report'),
    url(r'^request_report', report_views.request_report, name='request_report'),
    url(r'^export_csv', report_views.export_csv, name='export_csv'),

    url(r'^login/$',
        django.contrib.auth.views.login,
        {
            'template_name': 'app/login.html',
            'authentication_form': BootstrapAuthenticationForm,
            'extra_context':
            {
                'title': 'Log in',
                'year': timezone.now().year,
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
    url(r'^favicon\.ico$', RedirectView.as_view(url='static/favicon.ico')),
]
