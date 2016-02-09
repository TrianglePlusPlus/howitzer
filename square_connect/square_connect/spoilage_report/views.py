from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from django.db import models
from spoilage_report.models import SpoilageReport, SpoilageItem
import datetime

def spoilage_report(request):
    """Renders the reports page.
    request.POST dictionary keys:
        start_date
        end_date
        service"""
    assert isinstance(request, HttpRequest)
    # Check if they are searching for a report
    '''if request.POST.get('start_date', False):
        # They are searching for a report
        start_date = request.POST.get('start_date', None)
        end_date = request.POST.get('end_date', None)
        service = request.POST.get('service', None)
        reports = SpoilageReport.search_reports(start_date, end_date, service)
    else:
        reports = None'''
    report_start_date = datetime.datetime(2016, 1, 1) #datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    report_end_date = datetime.datetime(2016, 1, 30)
    service = 'midnight'
    reports = [SpoilageReport.search_reports(report_start_date, report_end_date, service)]
    # Check for invalid date
    return render(
        request,
        'spoilage_report/spoilage_report.html',
        context_instance = RequestContext(request,
        {
            'reports':reports,
            'title':'Report Viewer',
            'year':'Remember never give up.',
        })
    )