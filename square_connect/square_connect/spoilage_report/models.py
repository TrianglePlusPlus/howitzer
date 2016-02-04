from django.db import models
# Importing models from other apps
from app.models import Service
from data.transaction import LocationsRequest, PaymentRequest, format_money

class SpoilageReport(models.Model):
    # TODO
    date = models.DateField()
    service = models.ForeignKey("app.Service")
    
    @staticmethod
    def add_items_from_json_data(json_data, service):
        # TODO: Test this
        for transaction in json_data:
            for item in transaction['itemizations']:
                try:
                    spoiled = False
                    for discount in item['discounts']:
                        if discount['name'] == 'Spoil': spoiled = True
                    if spoiled:
                        # Check to see if that item is already in the database
                        if SpoilageItem.objects.filter(transaction_id=transaction["id"],  
                                name=item['name'], variant=item['item_variation_name']).count() > 0:
                            # The item already exists, don't save a new one
                            continue
                        # Get the report that the item should go on
                        transaction_date = SpoilageReport.get_associated_date(transaction["created_at"])
                        # Get or make the corresponding report
                        if SpoilageReport.objects.filter(date=report_date, service=service).count() > 0:
                            report = SpoilageReport.objects.get(service=service, date=report_date)
                        else:
                            report = SpoilageReport.objects.create(service=service, date=report_date)
                        spoiled_item = SpoilageItem()
                        spoiled_item.report_id = report.id
                        spoiled_item.transaction_id = transaction['id']
                        spoiled_item.name = item['name']
                        # 1 is an arbitrary cut off, typical variants are "Pumpkin"
                        # for a muffin for example
                        if len(item['item_variation_name']) > 1:
                            spoiled_item.variant = item['item_variation_name']
                        else:
                            spoiled_item.variant = ''
                        # 2 is an arbitrary cut off, normal SKUs should be 12
                        if len(item['item_detail']['sku']) > 2:
                            spoiled_item.sku = item['item_detail']['sku']
                        else:
                            spoiled_item.sku = ''
                        spoiled_item.price = format_money(item['single_quantity_money']['amount'])
                        spoiled_item.quantity = int(float(item['quantity']))
                        spoiled_item.save()
                except IndexError:
                    # There's nothing to do
                    pass

    def get_report(self, report_id):
        return SpoilageReport.objects.get(id=report_id)
        
    def get_associated_items(self):
        return SpoilageItem.objects.filter(pk=self.id)

    @staticmethod
    def search_reports(start_date, end_date, service=None):
        if service is not None:
            return SpoilageReport.objects.filter(date__range=(start_date, end_date), service__name=service)
        else:
            return SpoilageReport.objects.filter(date__range=(start_date, end_date))

    @staticmethod
    def get_associated_date(date_string):
        """ Gets the sales date for the input date string 
        @param dt: The date string in question, formatted in zulu time"""
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

class SpoilageItem(models.Model):
    """ A single spoiled item
    Part of a spoilage report """
    name = models.CharField(max_length=50, default='') 
    variant = models.CharField(max_length=100, default='')
    sku = models.CharField(max_length=12, default='') 
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    quantity = models.IntegerField(default=1)
    transaction_id = models.CharField(max_length=30, default='')
    # The report is the SpoilageReport which the item belongs to
    report = models.ForeignKey('SpoilageReport')
