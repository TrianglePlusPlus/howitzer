""" Sends emails with generated spoilage reports to the UM of each service """

from django.core.management.base import BaseCommand, CommandError
from django.contrib.sites.models import Site
from django.conf import settings # TODO: we need service_names
from app.models import Service
from mailer.models import MailingList, Person
from datetime import date, timedelta
from django.core.mail import send_mail
from spoilage_report.models import SpoilageReport, SpoilageItem
import datetime
from urllib.parse import quote

class Command(BaseCommand):
    help = "Sends emails with generated spoilage reports to the UM of each service"

    def handle(self, *args, **options):
        # Refresh the Services if necessary
        if Service.objects.count() == 0:
                Service.regenerate_services()

        # Run for each service with spoilage
        """ Service names in backend, exclude the * ones from the services list:
                midnight
                snaxa
                vittles
                ug
                mug
                hilltoss
                *the corp
                *storage
                *catering
                *students of georgetown incorporated
                *project whiteboard
        """
        # yesterday is the date of the reports being sent out, as they are sent out @ 4am
        yesterday = date.today() - timedelta(1)
        if yesterday.weekday() not in [5, 6]:
            excludes = ["the corp", "storage", "catering", "students of georgetown incorporated", "project whiteboard"]
        else:
            excludes = ["the corp", "storage", "catering", "students of georgetown incorporated", "project whiteboard", "mug", "hilltoss"]
        services = Service.objects.exclude(name__in=excludes)

        for service in services:
            mailing_list = MailingList.objects.get(service=service)

            # Get the spoilage report for the past day
            yesterday = date.today() - timedelta(days=1)
            report_url = "http://reports.thecorp.org/report?service=" + service.name + "&discount={discount}" + "&start_date=" + yesterday.strftime('%m/%d/%Y') + '&end_date=' + yesterday.strftime('%m/%d/%Y')

            for person in mailing_list.members:
                # Send a link to that report in an email
                report_url = report_url.format(discount=quote(person.discount))
                send_mail(
                    "Spoilage Report",
                    "Hello " + person.first_name + " " + person.last_name + "! Here is the spoilage report for " + settings.SERVICE_NAMES[service.name] + " on " + yesterday.strftime('%A, %d %B %Y') + " (yesterday):\n\n" + report_url,
                    settings.EMAIL_HOST_USER,
                    [person.email],
                    fail_silently=False
                )
