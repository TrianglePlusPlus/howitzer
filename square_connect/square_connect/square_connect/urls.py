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
# Uncomment the next lines to enable the admin:
from django.conf.urls import include
from django.contrib import admin
import app.views as app_views
import spoilage_report.views as spoilage_report_views
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', app_views.home, name='home'),
    url(r'^contact$', app_views.contact, name='contact'),
    url(r'^about', app_views.about, name='about'),
    url(r'^services', app_views.services, name='services'),
    url(r'^spoilage_report/$', spoilage_report_views.spoilage_report, name='spoilage_report'),
	url(r'^spoilage_report/([a-zA-Z]+)/([0-9]{4})/([0-9]{2})/([0-9]{2})/$', spoilage_report_views.spoilage_date, name='spoilage_date'),
    url(r'^spoilage_report/max/1996/02/15/$', spoilage_report_views.test_spoilage_report, name='test_spoilage_report'),
	url(r'^login/$',
        django.contrib.auth.views.login,
        {
            'template_name': 'app/login.html',
            'authentication_form': BootstrapAuthenticationForm,
            'extra_context':
            {
                'title':'Log in',
                'year':datetime.now().year,
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
)
