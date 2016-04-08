from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.template import RequestContext
from django.db import models
from spoilage_report.models import SpoilageReport, SpoilageItem
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers.json import DjangoJSONEncoder

import json

def spoilage_report(request):
    """Renders the reports page."""
    assert isinstance(request, HttpRequest)
    today = datetime.today().strftime("%m/%d/%Y")

    return render(
        request,
        'spoilage_report/spoilage_report.html',
        context_instance = RequestContext(request,
        {
            'today':today,
            'title':'Report Viewer',
            'year':'Remember never give up.',
        })
    )


def spoilage_report_date(request, service_location, start_year, start_month, start_day, end_year, end_month, end_day):
    """Renders the reports for a given date range and service, embedded in the url."""
    assert isinstance(request, HttpRequest)

    start_date = start_month + '/' + start_day + '/' + start_year
    end_date = end_month + '/' + end_day + '/' + end_year
    service = service_location

    return render(
        request,
        'spoilage_report/spoilage_report.html',
        context_instance = RequestContext(request,
        {
            'start_date': start_date,
            'end_date': end_date,
            'service': service,
            'title':'Report Viewer',
            'year':'Remember never give up.',
        })
    )

@csrf_exempt
# @require_POST ?
def request_report(request):
    """Requests the spoilage data.
    request.POST dictionary keys:
        start_date
        end_date
        service"""
    if request.method == "POST":
        #assert isinstance(request, HttpRequest)

        return_data = {}
        sum_total = 0

        # Check if they are searching for a report
        if request.POST.get('start_date', False) and request.POST.get('end_date', False):
            # They are searching for a report
            start_date = request.POST.get('start_date', None)
            end_date = request.POST.get('end_date', None)
            start_date = datetime.strptime(start_date, "%m/%d/%Y").date()
            end_date = datetime.strptime(end_date, "%m/%d/%Y").date()
            service = request.POST.get('service', None)
            reports = SpoilageReport.search_reports(start_date, end_date, service)
            reports_list = []
            if reports.count() > 0:
                for report in reports:
                    sum_total += report.get_total
                    reports_list.append(report.dictionary_form())
                return_data = {
                    "reports": reports_list,
                    "sum_total": sum_total
                }
        else:
            reports = None # is this really necessary?

        return HttpResponse(
            json.dumps(return_data, cls=DjangoJSONEncoder),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"POST method failed": "we have no data for you"}),
            content_type="application/json"
        )
