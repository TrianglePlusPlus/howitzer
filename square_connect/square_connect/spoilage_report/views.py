from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from django.db import models
from spoilage_report.models import SpoilageReport, SpoilageItem
import datetime

def spoilage_report(request):
    """Renders the reports page.
    request.POST dictionary keys:
        date
        service"""
    assert isinstance(request, HttpRequest)
    # Check if they are searching for a report
    if request.POST.get('date', False):
        # They are searching for a report
        date = request.POST.get('date', None)
        date = datetime.datetime.strptime(date, "%m/%d/%Y").date()
        service = request.POST.get('service', None)
        report = SpoilageReport.objects.filter(date=date, service__name=service)
        if report.count() > 0:
            report = SpoilageReport.objects.get(date=date, service__name=service)
    else:
        report = None
    return render(
        request,
        'spoilage_report/spoilage_report.html',
        context_instance = RequestContext(request,
        {
            'report':report,
            'title':'Report Viewer',
            'year':'Remember never give up.',
        })
    )
	
def spoilage_date(request, service_location, year, month, day):
	"""Renders the reports for a given date"""
	
	assert isinstance(request, HttpRequest)
	
	date = year + '-' + month + '-' + day
	service = service_location
	
	report = SpoilageReport.objects.filter(date=date, service__name=service)
	if report.count() > 0:
            report = SpoilageReport.objects.get(date=date, service__name=service)
	return render(
        request,
        'spoilage_report/spoilage_report.html',
        context_instance = RequestContext(request,
        {
            'report':report,
            'title':service + ' Report Viewer',
            'year':'Remember never give up.',
        })
    )
	
