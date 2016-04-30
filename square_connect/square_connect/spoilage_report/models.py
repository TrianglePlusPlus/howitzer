﻿from django.db import models
from django.utils.timezone import now as DjangoCurrentTime
import datetime
# Importing models from other apps
from app.models import Service
from data.transaction import LocationsRequest, PaymentRequest, format_money


class SpoilageReport(models.Model):
    # TODO
    date = models.DateField()
    service = models.ForeignKey("app.Service")

    @staticmethod
    def add_items_from_json_data(json_data, service):
        """ Extracts spoilage items from sales json and saves to a report
        @param json_data: The JSON object containing all of the transaction data
        @param service: A service object correspondinng to the sales data
        """
        for transaction in json_data:
            pending_items = {}
            # We first extract the spoilage transactions from the data set
            for item in transaction['itemizations']:
                try:
                    spoiled = False
                    for discount in item['discounts']:
                        if discount['name'] == 'Spoil': spoiled = True
                        # Vittles uses the discount "Expired" for spoilage
                        if discount['name'] == 'Expired': spoiled = True
                        # Vittles also uses "CREDITED Spoilage"
                        if discount['name'] == 'CREDITED Spoilage': spoiled = True
                    if spoiled:
                        hash_string = item['name']+item['item_variation_name']
                        if hash_string not in pending_items:
                            pending_items[hash_string] = [item]
                        else:
                            pending_items[hash_string].append(item)
                except IndexError:
                    # There's nothing to do
                    pass
            for item in pending_items:
                try:
                    features = pending_items[item][0]
                    item_total = 0
                    for elem in pending_items[item]:
                        item_total += int(float(elem['quantity']))
                    # Check to see if that item is already in the database
                    if SpoilageItem.objects.filter(transaction_id=transaction["id"],  
                            name=features['name'], variant=features['item_variation_name'], quantity=item_total).count() > 0:
                        # The item already exists, don't save a new one
                        continue
                    # Get the report that the item should go on
                    transaction_date = SpoilageReport.get_associated_date(transaction["created_at"])
                    # Get or make the corresponding report
                    if SpoilageReport.objects.filter(date=transaction_date, service=service).count() > 0:
                        report = SpoilageReport.objects.get(service=service, date=transaction_date)
                    else:
                        report = SpoilageReport.objects.create(service=service, date=transaction_date)
                    spoiled_item = SpoilageItem()
                    spoiled_item.report_id = report.id
                    spoiled_item.transaction_id = transaction['id']
                    # This next bit with the timezones is to that the database doesn't
                    # raise errors about naive datetimes. We set the timezone to UTC
                    utc_tz = datetime.timezone(datetime.timedelta(hours=0))
                    transaction_time = datetime.datetime.strptime(transaction['created_at'], "%Y-%m-%dT%H:%M:%SZ")
                    transaction_time = transaction_time.replace(tzinfo=utc_tz)
                    spoiled_item.transaction_time = transaction_time
                    spoiled_item.name = features['name']
                    # 1 is an arbitrary cut off, typical variants are "Pumpkin"
                    # for a muffin for example
                    if len(features['item_variation_name']) > 1:
                        spoiled_item.variant = features['item_variation_name']
                    else:
                        spoiled_item.variant = ''
                    # 2 is an arbitrary cut off, normal SKUs should be 12
                    if len(features['item_detail']['sku']) > 2:
                        spoiled_item.sku = features['item_detail']['sku']
                    else:
                        spoiled_item.sku = ''
                    spoiled_item.price = format_money(features['single_quantity_money']['amount'])
                    spoiled_item.quantity = item_total
                    spoiled_item.save()
                except IndexError:
                    # Nothing to do
                    pass

    @staticmethod
    def get_report(report_id):
        """ A shorthand method for getting reports by their ID
        @param report_id: The ID of the report to fetch
        @returns The report with the specified id
        """
        return SpoilageReport.objects.get(id=report_id)

    @property
    def get_associated_items(self):
        """ Finds the SpoilageItems associated with this report
        @returns The QuerySet containing all of the items associated with this report
        """
        # TODO: Test this
        return SpoilageItem.objects.filter(report=self).order_by('transaction_time')

    @property
    def get_size(self):
        """ Finds the size of the report in # of items
        @returns The size of the report
        """
        return self.get_associated_items.count()

    @property
    def get_total(self):
        """ Finds the total cost of all the itmes in this report
        @returns The total cost of all the items in the report (price * quantity)
        """
        total = 0
        for item in SpoilageItem.objects.filter(report=self):
            total += item.price * item.quantity
        return total

    @staticmethod
    def search_reports(start_date, end_date, service=None):
        """ Searches for reports in a given timeframe, service optional
        @param start_date: A datetime.date corresponding to the start date
        @param end_date: A datetime.date corresponding to the end date
        @param service: (Optional) The service to pull reports for
        @returns A QuerySet containing all of the reports from the date range (for a specified service)
        """
        if service is not None:
            return SpoilageReport.objects.filter(date__range=(start_date, end_date), service__name=service)
        else:
            return SpoilageReport.objects.filter(date__range=(start_date, end_date))

    @staticmethod
    def get_associated_date(date_string):
        """ Gets the sales date for the input date string
        Sales before 4/5 am EST belong to the previous day
        @param dt: The date string in question, FORMATTED IN ZULU TIME (UTC)
        @returns The 'sales' date that a date string belongs to
        """
        # Get the packages we need for this
        # We inject this package because it's not typically in use
        import datetime
        dt = datetime.datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ")
        if dt.hour < 9:
            # These sales are associated with the previous day
            return dt.date() - datetime.timedelta(days=1)
        else:
            # They are associated with the stated day
            return dt.date()

    def dictionary_form(self):
        """ Turns a report into a json-friendly dictionary that includes date, service, id, size, total, and a list of all items
        @returns a dictionary
        """
        return {
            "size": self.get_size,
            "total": self.get_total,
            "items": list(self.get_associated_items.values()),
        }

class SpoilageItem(models.Model):
    """ A single spoiled item
    Part of a spoilage report """
    name = models.CharField(max_length=50, default='')
    variant = models.CharField(max_length=100, default='')
    sku = models.CharField(max_length=12, default='')
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    quantity = models.IntegerField(default=1)
    transaction_id = models.CharField(max_length=30, default='')
    transaction_time = models.DateTimeField(default=DjangoCurrentTime)
    # The report is the SpoilageReport which the item belongs to
    report = models.ForeignKey('SpoilageReport')
