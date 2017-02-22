"""
@package square_connect.report.management.commands.get_recent_transactions
Gets the most recent transactions from the primary storefronts and adds any selected items to the report database.
We recommend that you run it in a cron job.
"""

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from app.models import Service
from report.models import Report, Item
from data.transaction import PaymentRequest
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = "Gets the last 200 transactions at each service and finds ___-marked items"

    # Allows input of report types to take in. Ex. spoilage and shift drinks.
    def add_arguments(self, parser):
        parser.add_argument('report_type', nargs='+')
        parser.add_argument('begin_time', nargs='+')
        parser.add_argument('end_time', nargs='+')

    def handle(self, *args, **options):
        # Refresh the Services if necessary
        if Service.objects.count() == 0:
                Service.regenerate_services()

        # Run for each service with discounts
        services = Service.objects.exclude(name__in=settings.SERVICE_EXCLUDES)

        for service in services:
            # Get the recent transactions for that service

            begin_time_str = options['begin_time']
            begin_time = datetime.strptime(begin_time_str[0], "%Y-%m-%dT%H:%M:%SZ")
            end_time_str = options['end_time']
            end_time = datetime.strptime(end_time_str[0], "%Y-%m-%dT%H:%M:%SZ")

            for time in (begin_time + timedelta(minutes=n) for n in range(0, int((end_time - begin_time).total_seconds() / 60.0), 30)):
                print(time)
                payment_request = PaymentRequest(merchant_id=service.merchant_id)

                payment_request.set_begin_time(time=time)
                payment_request.set_end_time(time=(time + timedelta(minutes=30)))

                payment_request.set_response_limit()
                payment_request.set_order_desc()
                payment_request.create_request()
                payment_request.send_request()

                sales_json = payment_request.response_json

                # Pass the sales to the report model so it can do its magic
                for report_type in options['report_type']:
                    Report.add_items_from_json_data(sales_json, service, discount=report_type)
