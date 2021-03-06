from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.template import RequestContext
from django.db import models
from django.conf import settings
import json
from report.models import Report, Item
from app.models import Service
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required

import json
import csv

@login_required
def report(request):
    """Renders the reports page.
    @param request: Takes in a request query to filter through the transaction data. Queries must have a date
    @param service_location: (GET parameter) Takes in Service name E.X. "coffee_shop"
    @param start_date: (GET parameter) Takes in the start date of the transactions
    @param end_date: (GET parameter) Takes in the end date of the transactions
    @returns filtered transaction data for today if no GET parameters, or based on date and service
    """
    assert isinstance(request, HttpRequest)

    today = datetime.today().strftime("%m/%d/%Y")
    services_json = json.dumps(settings.SERVICE_NAMES)


    if request.GET.get('service') or request.GET.get('discount') or request.GET.get('start_date') or request.GET.get('end_date'):
        service = request.GET.get('service', 'all')
        discount = request.GET.get('discount', 'all')
        start_date = request.GET.get('start_date', today)
        end_date = request.GET.get('end_date', today)

        return render(
            request,
            'report/report.html',
            {
                'start_date': start_date,
                'end_date': end_date,
                'service': service,
                'discount': discount,
                'services_json': services_json,
                'services': settings.SERVICES,
                'discounts': settings.DISCOUNTS,
                'discounts_umbrella': settings.DISCOUNTS_UMBRELLA_NAMES,
                'discounts_umbrella_values': settings.DISCOUNTS_UMBRELLA_VALUES,
                'report_relative_url': '/report',
                'title': 'Report Viewer',
                'year': 'Remember never give up.',
            }
        )
    else:
        return render(
            request,
            'report/report.html',
            {
                'services_json': services_json,
                'services': settings.SERVICES,
                'discounts': settings.DISCOUNTS,
                'discounts_umbrella': settings.DISCOUNTS_UMBRELLA_NAMES,
                'discounts_umbrella_values': settings.DISCOUNTS_UMBRELLA_VALUES,
                'report_relative_url': '/report',
                'today': today,
                'title': 'Report Viewer',
                'year': 'Remember never give up.',
            }
        )


def request_report(request):
    """Requests the report data.
    request.POST dictionary keys:
        start_date
        end_date
        service
        discount
    @param request: Takes in a request query to return a JSON dump of filtered transaction data.
    Queries must have a date range as well as service.
    @returns filtered transaction data based on a date
    """
    assert isinstance(request, HttpRequest)

    if request.method == "POST":
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
            service = request.POST.get('service', 'all')
            discount = request.POST.get('discount', 'all')
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

        return HttpResponse(
            json.dumps(return_data, cls=DjangoJSONEncoder),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

def export_csv(request):
    """Exports the report as a .CSV.
    request.POST dictionary keys:
        start_date
        end_date
        service
        discount
    @param request: Takes in a request query to return a CSV file of filtered transaction data.
    Queries must have a date range as well as service.
    @returns filtered transaction data based on a date range in .CSV format
    """
    assert isinstance(request, HttpRequest)

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
            discount = request.POST.get('discount', None)
            reports = Report.search_reports(start_date, end_date, service, discount)

        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(content_type='text/csv')
        if request.POST.get('discount', '') == 'all' or request.POST.get('discount', '') is None:
            discount_str = ''
        else:
            discount_str = ', filtered for the {discount} discount'.format(discount=request.POST.get('discount'))
        response['Content-Disposition'] = ('attachment; filename="Report for {service} from {start_date} to {end_date}'
                                           '{discount}.csv').format(
                service=settings.SERVICE_NAMES[service],
                start_date=request.POST.get('start_date', None),
                end_date=request.POST.get('end_date', None),
                discount=discount_str)
        writer = csv.writer(response)
        writer.writerow(['Service', 'Item', 'Variant', 'Price', 'Discount Type', 'Discount', 'Quantity', 'Transaction ID', 'Time'])
        if reports.count() > 0:
            for report in reports:
                for item in report.get_associated_items:
                    writer.writerow([
                        item.service,
                        item.name,
                        item.variant,
                        item.price,
                        item.discount,
                        item.discountcost,
                        item.quantity,
                        '=HYPERLINK("https://squareup.com/receipt/preview/' + item.transaction_id + '", "View Transaction")',
                        item.transaction_time])
                writer.writerow([])

        return response

    else:
        return HttpResponse(
            json.dumps({"POST method failed": "we have no data for you"}),
            content_type="application/json"
        )
