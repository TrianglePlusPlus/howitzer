from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.template import RequestContext
from django.db import models
from report.models import Report, Item
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers.json import DjangoJSONEncoder

import json

def report(request):
    """Renders the reports page."""
    assert isinstance(request, HttpRequest)
    today = datetime.today().strftime("%m/%d/%Y")

    return render(
        request,
        'report/report.html',
        context_instance = RequestContext(request,
        {
            'today':today,
            'title':'Report Viewer',
            'year':'Remember never give up.',
        })
    )

@csrf_exempt
# @require_POST ?
def request_custom_report(request):
    """Requests the report data.
    request.POST dictionary keys:
        start_date
        end_date
        service
        discount"""
    if request.method == "POST":
        #assert isinstance(request, HttpRequest)

        return_data = {}
        sum_total = 0
        discount_sum_total = 0

        # Check if they are searching for a report
        if request.POST.get('start_date', False) and request.POST.get('end_date', False):
            # They are searching for a report
            start_date = request.POST.get('start_date', None)
            end_date = request.POST.get('end_date', None)
            start_date = datetime.strptime(start_date, "%m/%d/%Y").date()
            end_date = datetime.strptime(end_date, "%m/%d/%Y").date()
            service = request.POST.get('service', None)
            discount = request.POST.get('discount', None)
            reports = Report.search_reports(start_date, end_date, service, discount)
            reports_list = []
            if reports.count() > 0:
                for report in reports:
                    sum_total += report.get_total
                    discount_sum_total += report.get_discount_total
                    reports_list.append(report.dictionary_form())
                return_data = {
                    "reports": reports_list,
                    "sum_total": sum_total,
                    "discount_sum_total": discount_sum_total
                }
        else:
            reports = None # is this really necessary?

        return HttpResponse(
            json.dumps(return_data, cls=DjangoJSONEncoder),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

def report_date(request, service_location, year, month, day):
	"""Renders the reports for a given date"""

	assert isinstance(request, HttpRequest)

	date = year + '-' + month + '-' + day
	service = service_location

	report = Report.objects.filter(date=date, service__name=service)
	if report.count() > 0:
            report = Report.objects.get(date=date, service__name=service)
	return render(
        request,
        'report/report.html',
        context_instance = RequestContext(request,
        {
            'report':report,
            'title':service + ' Report Viewer',
            'year':'Remember never give up.',
        })
    )

