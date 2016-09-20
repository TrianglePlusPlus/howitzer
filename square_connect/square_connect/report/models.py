from django.db import models
from django.utils.timezone import now as DjangoCurrentTime
import datetime
# Importing models from other apps
from app.models import Service
from data.transaction import LocationsRequest, PaymentRequest, format_money


class Report(models.Model):
    # TODO
    date = models.DateField()
    service = models.ForeignKey("app.Service")
    discount_label = models.CharField(max_length=50, default='')

    @staticmethod
    def add_items_from_json_data(json_data, service, discount='All'):
        """ Extracts items from sales json and saves to a report
        @param json_data: The JSON object containing all of the transaction data
        @param service: A service object correspondinng to the sales data
		@param discount: The discount tag that is being searched for. For example: 'Spoil', 'Cup Reuse'
        """
        
        """
        List of discounts:
        TODO: Check to see if there are more discounts
		
		'Employee Discount - Coffee'
		'Spoil'
		'Cup Reuse'
		'Dollar FIDDY Off Dat Sambo'
		'Shift Drink - UG'
		'Shift Drink - Vital Vittles'
		'Shift Drink - Accounting'
		'Shift Drink - Accounting'
		'Shift Drink - MUG'
		'Shift Drink - Hoya Snaxa'
		'Shift Drink - ITM'
		
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
                            if entry['name'] == discount: found = True
                            # This is to catch all shift drinks (unless we only want shift drinks per service?). I'm probably missing some
                            elif (entry['name'] == 'Shift Drink - UG' or 'Shift Drink - Vital Vittles' or 'Shift Drink - Accounting' or 'Shift Drink - MUG' or 'Shift Drink - Hoya Snaxa' or 'Shift Drink - ITM'):
                                found = True
                    if found:
                        # Check to see if that item is already in the database
                        
                        if Item.objects.filter(transaction_id=transaction["id"],
                                name=item['name'], variant=item['item_variation_name']).count() > 0:
                            # The item already exists, don't save a new one
                            continue
					    
                        # Get the report that the item should go on
                        transaction_date = Report.get_associated_date(transaction["created_at"])
                        # Get or make the corresponding report
                        if Report.objects.filter(date=transaction_date, service=service, discount_label=label).count() > 0:
                            report = Report.objects.get(service=service, date=transaction_date, discount_label=label)
                        else:
                            report = Report.objects.create(service=service, date=transaction_date, discount_label=label)
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
                        report_item.label = label
                        # 1 is an arbitrary cut off, typical variants are "Pumpkin"
                        # for a muffin for example
                        """
                        if len(item['item_variation_name']) > 1:
                            report_item.variant = item['item_variation_name']
                        else:
                            report_item.variant = ''
						"""
                        # 2 is an arbitrary cut off, normal SKUs should be 12
                        if len(item['item_detail']['sku']) > 2:
                            report_item.sku = item['item_detail']['sku']
                        else:
                            report_item.sku = ''
                        report_item.price = format_money(item['single_quantity_money']['amount'])
                        report_item.quantity = int(float(item['quantity']))
                        report_item.save()
                except IndexError:
                    # There's nothing to do
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
        """ Finds the SpoilageItems associated with this report
        @returns The QuerySet containing all of the items associated with this report
        """
        # TODO: Test this
        return Item.objects.filter(report=self).order_by('transaction_time')

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
        for item in Item.objects.filter(report=self):
            total += item.price * item.quantity
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
        if discount is not None:
            if service is not None:
                return Report.objects.filter(date__range=(start_date, end_date), service__name=service, discount_label__name=discount)
            else:
                return Report.objects.filter(date__range=(start_date, end_date))
        else:
            if service is not None:
                return Report.objects.filter(date__range=(start_date, end_date), service__name=service)
            else:
                return Report.objects.filter(date__range=(start_date, end_date))

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

class Item(models.Model):
    """ A single item
    Part of a report """
    name = models.CharField(max_length=50, default='')
    variant = models.CharField(max_length=100, default='')
    sku = models.CharField(max_length=12, default='')
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    quantity = models.IntegerField(default=1)
    transaction_id = models.CharField(max_length=30, default='')
    transaction_time = models.DateTimeField(default=DjangoCurrentTime)
    # The report is the Report which the item belongs to
    report = models.ForeignKey('Report')
    label = models.CharField(max_length=50, default='')
