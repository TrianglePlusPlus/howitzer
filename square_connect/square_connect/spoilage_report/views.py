<<<<<<< HEAD
from django.shortcuts import render
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
=======
﻿from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpRequest
from django.template import RequestContext

# Create your views here.

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'spoilage_report/index.html',
        context_instance = RequestContext(request,
        {
            'title':'Home Page',
            'year': '20XX',

        })
    )



"""
 .----------------.  .----------------.  .----------------.  .----------------.   .----------------.  .----------------.  .----------------. 
| .--------------. || .--------------. || .--------------. || .--------------. | | .--------------. || .--------------. || .--------------. |
| |  _________   | || | _____  _____ | || |     ______   | || |  ___  ____   | | | |  ____  ____  | || |     ____     | || | _____  _____ | |
| | |_   ___  |  | || ||_   _||_   _|| || |   .' ___  |  | || | |_  ||_  _|  | | | | |_  _||_  _| | || |   .'    `.   | || ||_   _||_   _|| |
| |   | |_  \_|  | || |  | |    | |  | || |  / .'   \_|  | || |   | |_/ /    | | | |   \ \  / /   | || |  /  .--.  \  | || |  | |    | |  | |
| |   |  _|      | || |  | '    ' |  | || |  | |         | || |   |  __'.    | | | |    \ \/ /    | || |  | |    | |  | || |  | '    ' |  | |
| |  _| |_       | || |   \ `--' /   | || |  \ `.___.'\  | || |  _| |  \ \_  | | | |    _|  |_    | || |  \  `--'  /  | || |   \ `--' /   | |
| | |_____|      | || |    `.__.'    | || |   `._____.'  | || | |____||____| | | | |   |______|   | || |   `.____.'   | || |    `.__.'    | |
| |              | || |              | || |              | || |              | | | |              | || |              | || |              | |
| '--------------' || '--------------' || '--------------' || '--------------' | | '--------------' || '--------------' || '--------------' |
 '----------------'  '----------------'  '----------------'  '----------------'   '----------------'  '----------------'  '----------------' 
 """
>>>>>>> a08555e82e59f506aa629d92967658822335e94f
