""" Gets the most recent transactions from the 6 primary storefronts
and adds any selected items to the report databse """

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from app.models import Service
from report.models import Report, Item
from data.transaction import PaymentRequest


class Command(BaseCommand):
    help = "Gets the last 200 transactions at each service and finds ___-marked items"

    # Allows input of report types to take in. Ex. spoilage and shift drinks.
    def add_arguments(self, parser):
        parser.add_argument('report_type', nargs='+')

    def handle(self, *args, **options):
        # Refresh the Services if necessary
        if Service.objects.count() == 0:
                Service.regenerate_services()

        # Run for each service with discounts
        services = Service.objects.exclude(name__in=settings.SERVICE_EXCLUDES)

        for service in services:
            # Get the recent transactions for that service
            sales_json = PaymentRequest(merchant_id=service.merchant_id).auto()

            # Pass the sales to the report model so it can do its magic
            for report_type in options['report_type']:
                Report.add_items_from_json_data(sales_json, service)
