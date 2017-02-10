"""
@package square_connect.mailer.management.commands.send_emails
Sends emails with generated reports to the UM of each service.
We recommend that you run it in a cron job.
"""

from django.core.management.base import BaseCommand, CommandError
from django.contrib.sites.models import Site
from django.conf import settings # TODO: we need service_names
from app.models import Service
from mailer.models import MailingList, Person
from datetime import date, timedelta
from django.core.mail import send_mail
import datetime
import urllib.parse

class Command(BaseCommand):
    help = "Sends emails with generated reports to the UM of each service"

    def handle(self, *args, **options):
        # Refresh the Services if necessary
        if Service.objects.count() == 0:
                Service.regenerate_services()

        # Run for each service with discounted items
        # yesterday is the date of the reports being sent out, as they are sent out @ 4am
        yesterday = date.today() - timedelta(1)
        if yesterday.weekday() not in [5, 6]:
            excludes = settings.SERVICE_EXCLUDES
        else:
            excludes = settings.SERVICE_EXCLUDES_WEEKEND
        services = Service.objects.exclude(name__in=excludes)

        for service in services:
            mailing_list = MailingList.objects.get(service=service)

            # Get the report for the past day
            yesterday = date.today() - timedelta(days=1)
            parameters = {
                'service': service.name,
                'discount': '',
                'start_date': yesterday.strftime('%m/%d/%Y'),
                'end_date': yesterday.strftime('%m/%d/%Y'),
            }

            for person in mailing_list.members:
                # Send a link to that report in an email
                parameters['discount'] = person.discount
                parameter_values = urllib.parse.unquote(urllib.parse.urlencode(parameters))
                report_url = settings.REPORT_BASE_URL + '?' + parameter_values
                message = (
                    "Hello " + person.first_name + " " + person.last_name +
                    "! Here is the discounts report for " + settings.SERVICE_NAMES[service.name] +
                    " on " + yesterday.strftime('%A, %d %B %Y') + " (yesterday):\n\n" + report_url
                )
                send_mail(
                    "Discounts Report",
                    message,
                    settings.EMAIL_HOST_USER,
                    [person.email],
                    fail_silently=False
                )
