from django.shortcuts import render
from spoilage_report.models import SpoilageReport, SpoilageItem

def reports(request):
    """Renders the reports page."""
    assert isinstance(request, HttpRequest)
    # Check if they are searching for a report
    if request.POST.get('start_date', False):
        # They are searching for a report
        start_date = request.POST.get('start_date', None)
        end_date = request.POST.get('end_date', None)
        service = request.POST.get('service', None)
        reports = SpoilageReport.search_reports(start_date, end_date, service)
    return render(
        request,
        'spoilage_report/reports.html',
        context_instance = RequestContext(request,
        {
            'title':'Report Viewer',
            'year':'Remember never give up.',
        })
    )