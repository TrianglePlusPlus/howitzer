""" Sends emails with generated spoilage reports to the UM of each service """

from django.core.management.base import BaseCommand, CommandError
from django.contrib.sites.models import Site
from app.models import Service
from datetime import date
from django.core.mail import send_mail
from spoilage_report.models import SpoilageReport, SpoilageItem

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
        excludes = ["the corp", "storage", "catering", "students of georgetown incorporated", "project whiteboard"]
        services = Service.objects.exclude(name__in=excludes)

        for service in services:
            # Get the spoilage report for the past day
            # report_url = Site.objects.get_current().domain + "/spoilage_report/" + service.name + "/" + date.today().strftime('%Y/%m/%d') + '/'
            report_url = "http://localhost:8111/spoilage_report/" + service.name + "/" + date.today().strftime('%Y/%m/%d') + '/' + date.today().strftime('%Y/%m/%d') + '/'

            # Send a link to that report in an email
            send_mail("hello ( ͡° ͜ʖ ͡°)", "go to this url!:\n" + report_url, "bodonicreativedesign@gmail.com", ["peter@thecorp.org"], fail_silently=False)
