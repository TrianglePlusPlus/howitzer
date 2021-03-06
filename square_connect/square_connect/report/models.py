from django.db import models
from django.db.models import Q
from django.conf import settings
from django.utils.timezone import now as DjangoCurrentTime
import datetime
# Importing models from other apps
from app.models import Service
from data.transaction import LocationsRequest, PaymentRequest, format_money

class Report(models.Model):
    """ A collection of Items. Used to construct reports data from Squares Connect API JSON and to pull reports when searching. """
    date = models.DateField()
    service = models.ForeignKey("app.Service")
    discount_label = models.CharField(max_length=50, default='')

    @staticmethod
    def add_items_from_json_data(json_data, service_name, discount='All'):
        """ Extracts items from sales json and saves to a report
        @param json_data: The JSON object containing all of the transaction data
        @param service_name: A service object correspondinng to the sales data
        @param discount: The discount tag that is being searched for. For example: 'Spoil', 'Cup Reuse'
        """

        for transaction in json_data:
            for item in transaction['itemizations']:
                try:
                    found = False
                    if discount == 'All':
                        if len(item['discounts']) != 0:
                            found = True
                            label = item['discounts'][0]['name']
                    else:
                        for entry in item['discounts']:
                            if entry['name'] == discount:
                                found = True
                    if found:
                        if not 'item_variation_name' in item:
                            item['item_variation_name'] = ''

                        # Check to see if that item is already in the database
                        try:
                            if Item.objects.filter(transaction_id=transaction["id"],
                                                   name=item['name'], variant=item['item_variation_name']).count() > 0:
                                # The item already exists, don't save a new one
                                continue
                        except KeyError as e:
                            print("KeyError found: " + str(e))

                        # Get the report that the item should go on
                        transaction_date = Report.get_associated_date(transaction["created_at"])
                        # Get or make the corresponding report
                        if Report.objects.filter(date=transaction_date, service=service_name,
                                                 discount_label=label).count() > 0:
                            report = Report.objects.get(service=service_name, date=transaction_date,
                                                        discount_label=label)
                        else:
                            report = Report.objects.create(service=service_name, date=transaction_date,
                                                           discount_label=label)
                        report_item = Item()
                        report_item.report_id = report.id
                        report_item.transaction_id = transaction['id']
                        # This next bit with the timezones is to that the database doesn't
                        # raise errors about naive datetimes. We set the timezone to UTC
                        utc_tz = datetime.timezone(datetime.timedelta(hours=0))
                        transaction_time = datetime.datetime.strptime(transaction['created_at'], "%Y-%m-%dT%H:%M:%SZ")
                        transaction_time = transaction_time.replace(tzinfo=utc_tz)
                        report_item.transaction_time = transaction_time
                        report_item.name = item['name']
                        report_item.discount = label

                        # Formats the service names correctly from all lower case to either all upper
                        # case (for MUG and UG) or Title Case
                        if len(str(service_name.name)) > 3:
                            report_item.service = str(service_name.name).title()
                        else:
                            report_item.service = str(service_name.name).upper()

                        # 1 is an arbitrary cut off, typical variants are "Pumpkin"
                        # for a muffin for example

                        try:
                            if len(item['item_variation_name']) > 1:
                                report_item.variant = item['item_variation_name']
                            else:
                                report_item.variant = ''
                        except KeyError as e:
                            print("KeyError found: " + str(e))
                        # 2 is an arbitrary cut off, normal SKUs should be 12
                        if len(item['item_detail']['sku']) > 2:
                            report_item.sku = item['item_detail']['sku']
                        else:
                            report_item.sku = ''
                        report_item.price = format_money(item['single_quantity_money']['amount'])
                        report_item.quantity = int(float(item['quantity']))
                        report_item.discountcost = format_money(abs(item['discount_money']['amount'])/report_item.quantity)
                        report_item.save()
                except IndexError as e:
                    print(e)
                    pass

    @staticmethod
    def get_report(report_id):
        """ A shorthand method for getting reports by their ID
        @param report_id: The ID of the report to fetch
        @returns The report with the specified id
        """
        return Report.objects.get(id=report_id)

    @property
    def get_associated_items(self):
        """ Finds the Items associated with this report
        @returns The QuerySet containing all of the items associated with this report
        """
        return Item.objects.filter(report=self).order_by('transaction_time')

    @property
    def get_size(self):
        """ Finds the size of the report in # of items
        @returns The size of the report
        """
        return self.get_associated_items.count()

    @property
    def get_total(self):
        """ Finds the total cost of all the items in this report
        @returns The total cost of all the items in the report (price * quantity)
        """
        total = 0
        for item in Item.objects.filter(report=self):
            total += item.price * item.quantity
        return total

    @property
    def get_discount_total(self):
        """ Finds the total discounts across a report
        @returns The total discounts (cost * quantity)
        """

        total = 0
        for item in Item.objects.filter(report=self):
            total += item.discountcost * item.quantity
        return total

    @staticmethod
    def search_reports(start_date, end_date, service=None, discount=None):
        """ Searches for reports in a given timeframe, service optional. Discount optional
        @param start_date: A datetime.date corresponding to the start date
        @param end_date: A datetime.date corresponding to the end date
        @param service: (Optional) The service to pull reports for
        @param discount: (Optional) The discount to pull reports for
        @returns A QuerySet containing all of the reports from the date range (for a specified service)
        """
        if (discount is not None) and (discount != 'all'):
            if (service is not None) and (service != 'all'):
                """ The following code bundles discount tags """
                if discount in settings.DISCOUNT_CATEGORIES:
                    # For all of the discounts in that category:
                    # Turn list of values into a query, made up of OR'd Q objects
                    queries = [Q(discount_label=d) for d in settings.DISCOUNTS_BY_CATEGORY[discount]]
                    query = Q()
                    for q in queries:
                        query |= q

                    # Query the model
                    return Report.objects.filter(Q(date__range=(start_date, end_date)),
                                                 Q(service__name=service),
                                                 query)
                else:
                    # If discount is not an umbrella category
                    return Report.objects.filter(date__range=(start_date, end_date),
                                                 service__name=service, discount_label=discount)
            else:
                """ The following code shows how to bundle discount tags for a particular service """
                if discount in settings.DISCOUNT_CATEGORIES:
                    # For all of the discounts in that category:
                    # Turn list of values into a query, made up of OR'd Q objects
                    queries = [Q(discount_label=d) for d in settings.DISCOUNTS_BY_CATEGORY[discount]]
                    query = Q()
                    for q in queries:
                        query |= q

                    # Query the model
                    return Report.objects.filter(Q(date__range=(start_date, end_date)),
                                                 query)
                else:
                    # If discount is not an umbrella category
                    return Report.objects.filter(date__range=(start_date, end_date), discount_label=discount)
        else:
            if (service is not None) and (service != 'all'):
                return Report.objects.filter(date__range=(start_date, end_date), service__name=service)
            else:
                return Report.objects.filter(date__range=(start_date, end_date))

    @staticmethod
    def get_associated_date(date_string):
        """ Gets the sales date for the input date string
        Sales before 4/5 am EST belong to the previous day
        @param date_string: The date string in question, FORMATTED IN ZULU TIME (UTC)
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
        """ Turns a report into a json-friendly dictionary that includes date, service, id, size, total,
        and a list of all items
        @returns a dictionary
        """
        return {
            "size": self.get_size,
            "total": self.get_total,
            "discount_total": self.get_discount_total,
            "items": list(self.get_associated_items.values()),
        }


class Discounts(models.Model):
    """ Handles individual discounts"""
    name = models.CharField(max_length=50, default='')
    amount = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)


class Item(models.Model):
    """ A single item. Part of a report. """
    name = models.CharField(max_length=50, default='')
    variant = models.CharField(max_length=100, default='')
    sku = models.CharField(max_length=12, default='')
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    quantity = models.IntegerField(default=1)
    transaction_id = models.CharField(max_length=30, default='')
    transaction_time = models.DateTimeField(default=DjangoCurrentTime)
    # The report is the Report which the item belongs to
    report = models.ForeignKey('Report')
    discount = models.CharField(max_length=50, default='')
    discountcost = models.DecimalField(max_digits=6, decimal_places=2, default=4.00)
    service = models.CharField(max_length=50, default='')
    # Discounts have a many to many relationship with the discounts model.
    # This is to ensure that multiple discounts can be caught (1 item 2 discounts applied)
    discounts = models.ManyToManyField(Discounts)
