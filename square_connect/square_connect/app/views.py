"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
# For security
from django.template.context_processors import csrf
# Our imports
from data.transaction import PaymentRequest, LocationsRequest
from spoilage_report.models import SpoilageReport, SpoilageItem
from app.models import Service

def home(request):
    """Renders the home page."""
    query_results = SpoilageReport.objects.all(),
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        context_instance = RequestContext(request,
        {
            'title':'Home Page',
            'year':'Remember never give up.',
        })
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        context_instance = RequestContext(request,
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':'Remember never give up.',
        })
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        context_instance = RequestContext(request,
        {
            'title':'About',
            'message':'Your application description page.',
            'year':'Remember never give up.',
        })
    )

def services(request):
    """Shows the services and their associated merchant IDs
    Can be used to refresh the merchant IDs
    """
    assert isinstance(request, HttpRequest)
    if request.POST.get('regenerate', False):
        Service.regenerate_services()
    return render(
        request,
        'app/services.html',
        context_instance = RequestContext(request,
        {
            'title':'Services',
            'services':Service.objects.all(),
        })

    )