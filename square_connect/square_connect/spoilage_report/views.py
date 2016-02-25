from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from django.db import models
from spoilage_report.models import SpoilageReport, SpoilageItem
from datetime import datetime

def spoilage_report(request):
    """Renders the reports page.
    request.POST dictionary keys:
        start_date
        end_date
        service"""
    assert isinstance(request, HttpRequest)
    today = datetime.today().strftime("%m/%d/%Y")
    # Check if they are searching for a report
    if request.POST.get('start_date', False) and request.POST.get('end_date', False):
        # They are searching for a report
        start_date = request.POST.get('start_date', None)
        end_date = request.POST.get('end_date', None)
        start_date = datetime.strptime(start_date, "%m/%d/%Y").date()
        end_date = datetime.strptime(end_date, "%m/%d/%Y").date()
        service = request.POST.get('service', None)
        reports = SpoilageReport.search_reports(start_date, end_date, service)
        if reports.count() > 0:
            reports = SpoilageReport.objects.get(date__gte=start_date, date__lte=end_date, service__name=service)
    else:
        report = None
    return render(
        request,
        'spoilage_report/spoilage_report.html',
        context_instance = RequestContext(request,
        {
            'report':reports,
            'today':today,
            'title':'Report Viewer',
            'year':'Remember never give up.',
        })
    )