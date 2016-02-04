from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from spoilage_report.models import SpoilageReport, SpoilageItem

def reports(request):
    """Renders the reports page.
    request.POST dictionary keys:
        start_date
        end_date
        service"""
    assert isinstance(request, HttpRequest)
    # Check if they are searching for a report
    if request.POST.get('start_date', False):
        # They are searching for a report
        start_date = request.POST.get('start_date', None)
        end_date = request.POST.get('end_date', None)
        service = request.POST.get('service', None)
        reports = SpoilageReport.search_reports(start_date, end_date, service)
    else:
        reports = None
    return render(
        request,
        'spoilage_report/reports.html',
        context_instance = RequestContext(request,
        {
            'reports':reports,
            'title':'Report Viewer',
            'year':'Remember never give up.',
        })
    )

def spoilage_report(request):
    """Renders the reports page.
    request.POST dictionary keys:
        start_date
        end_date
        service"""
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