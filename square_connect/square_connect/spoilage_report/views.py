from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.template import RequestContext
from django.db import models
from app.models import service_names
from spoilage_report.models import SpoilageReport, SpoilageItem
from datetime import datetime
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required

import json, csv

@login_required
def spoilage_report(request):
    """Renders the reports page.
    @param request: Takes in a request query to filter through the spoilage data. Queries must have a date
    @param service_location: (GET parameter) Takes in Corp Service E.X. "mug"
    @param start_year: (GET parameter) Takes in the start year of the spoilage
    @param start_month: (GET parameter) Takes in the start month of the spoilage
    @param start_day: (GET parameter) Takes in the start day of the spoilage
    @param end_year: (GET parameter) Takes in the end year of the spoilage
    @param end_month: (GET parameter) Takes in the end month of the spoilage
    @param end_day: (GET parameter) Takes in the end day of the spoilage
    @returns filtered spoilage data for today if no GET parameters, or based on date and service
    """
    assert isinstance(request, HttpRequest)

    if request.GET.get('service', None):
        service = request.GET.get('service', None)
        # TODO: discount = request.GET.get('discount', None)
        start_date = request.GET.get('start_date', None)
        end_date = request.GET.get('end_date', None)

        return render(
            request,
            'spoilage_report/spoilage_report.html',
            {
                'start_date': start_date,
                'end_date': end_date,
                'service': service,
                'title':'Report Viewer',
                'year':'Remember never give up.',
            }
        )
    else:
        today = datetime.today().strftime("%m/%d/%Y")
        return render(
            request,
            'spoilage_report/spoilage_report.html',
            {
                'today':today,
                'title':'Report Viewer',
                'year':'Remember never give up.',
            }
        )

def request_report(request):
    """Requests the spoilage data.
    request.POST dictionary keys:
        start_date
        end_date
        service
    @param request: Takes in a request query to return a JSON dump of filtered spoilage data. Queries must have a date range as well as service
    @returns filtered spoilage data based on a date
    """
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

def export_csv(request):
    """Exports the report as a .CSV.
    request.POST dictionary keys:
        start_date
        end_date
        service
    @param request: Takes in a request query to return a CSV file of filtered spoilage data. Queries must have a date range as well as service
    @returns filtered spoilage data based on a date range in .CSV format
    """
    if request.method == "POST":
        return_data = {}
        sum_total = 0

        # Check if they are searching for a report
        reports = []
        if request.POST.get('start_date', False) and request.POST.get('end_date', False):
            # They are searching for a report
            start_date = request.POST.get('start_date', None)
            end_date = request.POST.get('end_date', None)
            start_date = datetime.strptime(start_date, "%m/%d/%Y").date()
            end_date = datetime.strptime(end_date, "%m/%d/%Y").date()
            service = request.POST.get('service', None)
            reports = SpoilageReport.search_reports(start_date, end_date, service)

        # TODO: use dictionary_form and csv.DictWriter?
        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Report for ' + service_names[service] + ' from ' + request.POST.get('start_date', None) + ' to ' + request.POST.get('end_date', None) + '.csv"'
        writer = csv.writer(response)
        writer.writerow(['Item', 'Variant', 'Price', 'Quantity', 'Transaction ID', 'Time'])
        if reports.count() > 0:
            for report in reports:
                for item in report.get_associated_items:
                    writer.writerow([item.name, item.variant, item.price, item.quantity, '=HYPERLINK("https://squareup.com/receipt/preview/' + item.transaction_id + '", "View Transaction")', item.transaction_time])
                writer.writerow([])

        return response

    else:
        return HttpResponse(
            json.dumps({"POST method failed": "we have no data for you"}),
            content_type="application/json"
        )
