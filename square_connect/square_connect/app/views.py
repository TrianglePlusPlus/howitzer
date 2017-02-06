"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from datetime import datetime
# For security
from django.template.context_processors import csrf
# Our imports
from data.transaction import PaymentRequest, LocationsRequest
from app.models import Service

def home(request):
    """Renders the home page.
	@param request: Takes in a request for the home page
	@returns home page
	"""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':'Remember never give up.',
        }
    )

@login_required
def contact(request):
    """Renders the contact page.
	@param request: Takes in request for the contact page
	@returns contact page
	"""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'year':'Remember never give up.',
        }
    )

@login_required
def about(request):
    """Renders the about page.
	@param request: Takes in request for the about page
	@returns about page
	"""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'year':'Remember never give up.',
        }
    )

@staff_member_required
def services(request):
    """Shows the services and their associated merchant IDs
    Can be used to refresh the merchant IDs
	@param request: Takes in request for the services page
	@returns services page. Can refresh merchant IDs
    """
    assert isinstance(request, HttpRequest)
    if request.POST.get('regenerate', False):
        Service.regenerate_services()
    return render(
        request,
        'app/services.html',
        {
            'title':'Services',
            'services':Service.objects.all(),
        }

    )
