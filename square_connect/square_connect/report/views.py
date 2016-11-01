from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.template import RequestContext
from django.db import models
from report.models import Report, Item
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers.json import DjangoJSONEncoder

import json
from urllib.parse import unquote


def report(request):
    """Renders the reports page."""
    assert isinstance(request, HttpRequest)
    today = datetime.today().strftime("%m/%d/%Y")

    return render(
        request,
        'report/report.html',
        context_instance = RequestContext(request,
        {
            'today': today,
            'title': 'Report Viewer',
            'year': 'Remember never give up.',
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
        # assert isinstance(request, HttpRequest)

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
            reports = None  # is this really necessary?

        return HttpResponse(
            json.dumps(return_data, cls=DjangoJSONEncoder),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


def report_date(request, service_location, discount_label, start_year, start_month, start_day, end_year, end_month, end_day):
    """Renders the reports for a given date
    @param request: Takes a request for spoilage
    @param service_location: Takes in Corp Service E.X. "mug"
    @param discount_label: Takes in a discount to search for E.X. "spoil"
    @param start_year: Takes in the start year of the spoilage
    @param start_month: Takes in the start month of the spoilage
    @param start_day: Takes in the start day of the spoilage
    @param end_year: Takes in the end year of the spoilage
    @param end_month: Takes in the end month of the spoilage
    @param end_day: Takes in the end day of the spoilage
    @returns filtered spoilage data based on date and service
    """

    assert isinstance(request, HttpRequest)

    start_date = start_month + '/' + start_day + '/' + start_year
    end_date = end_month + '/' + end_day + '/' + end_year
    discount = unquote(discount_label)
    service = service_location

    return render(
        request,
        'report/report.html',
        context_instance = RequestContext(request,
        {
            'start_date': start_date,
            'end_date': end_date,
            'service': service,
            'discount': discount,
            'title': service + ' Report Viewer',
            'year':'Remember never give up.',
        })
    )

