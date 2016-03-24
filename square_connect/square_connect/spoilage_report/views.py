from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.template import RequestContext
from django.db import models
from spoilage_report.models import SpoilageReport, SpoilageItem
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers.json import DjangoJSONEncoder

import json

def spoilage_report(request):
    """Renders the reports page.
    request.POST dictionary keys:
        start_date
        end_date
        service"""
    assert isinstance(request, HttpRequest)
    today = datetime.today().strftime("%m/%d/%Y")
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
        if reports.count() > 0:
            first_report = reports[0]
            for report in reports:
                sum_total += report.get_total
        else:
            first_report = None
    else:
        first_report = None
        reports = None

    return render(
        request,
        'spoilage_report/spoilage_report.html',
        context_instance = RequestContext(request,
        {
            'first_report':first_report,
            'reports':reports,
            'sum_total':sum_total,
            'today':today,
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
            if reports.count() > 0:
                for report in reports:
                    sum_total += report.get_total
                return_data = {
                    "reports": list(reports.values()), # bad idea?
                    "sum_total": sum_total
                }
        else:
            reports = None # is this really necessary?

        return HttpResponse(
            json.dumps(return_data, cls=DjangoJSONEncoder), # can serialize dictionary, but need to serialize list of dictionaries, and also dictionary including list of dictionaries (possibly)
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )