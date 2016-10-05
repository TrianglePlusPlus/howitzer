""" Sends emails with generated spoilage reports to the UM of each service """

from django.core.management.base import BaseCommand, CommandError
from django.contrib.sites.models import Site
from app.models import Service
from mailer.models import MailingList, Person
from datetime import date, timedelta
from django.core.mail import send_mail
from spoilage_report.models import SpoilageReport, SpoilageItem
import datetime

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
        if datetime.datetime.weekday():
            excludes = ["the corp", "storage", "catering", "students of georgetown incorporated", "project whiteboard"]
        else:
            excludes = ["the corp", "storage", "catering", "students of georgetown incorporated", "project whiteboard", "mug", "hilltoss"]
        services = Service.objects.exclude(name__in=excludes)

        for service in services:
            mailing_list = MailingList.objects.get(service=service)
            for person in mailing_list.members:
                # Get the spoilage report for the past day
                yesterday = date.today() - timedelta(days=1)
                report_url = "http://reports.thecorp.org/spoilage_report/" + service.name + "/" + yesterday.strftime('%Y/%m/%d') + '/' + yesterday.strftime('%Y/%m/%d') + '/'

                service_names = {
                    "mug": "MUG",
                    "vittles": "Vital Vittles",
                    "snaxa": "Hoya Snaxa",
                    "ug": "Uncommon Grounds",
                    "midnight": "Midnight Mug",
                    "hilltoss": "Hilltoss",
                }

                # Send a link to that report in an email
                send_mail(
                    "Spoilage Report",
                    "Hello " + person.first_name + " " + person.last_name + "! Here is the spoilage report for " + service_names[service.name] + " on " + yesterday.strftime('%A, %d %B %Y') + " (yesterday):\n\n" + report_url,
                    "reports@thecorp.org",
                    [person.email],
                    fail_silently=False
                )
