""" Gets the most recent transactions from the 6 primary storefronts
and adds any spoiled items to the spoilage databse """

from app.models import Service
from spoilage_report.models import SpoilageReport, SpoilageItem
import datetime

# Run for each service
services = Service.objects.all()


# Check to see if a report exists for today
current_time = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
report_date = SpoilageReport.get_associated_date(current_time)

if SpoilageReport.objects.filter(date=report_date).count() > 0:
    report = SpoilageReport.objects.get(date=report_date)
else:
    report = SpoilageReport()
    report.date = report_date
    report
