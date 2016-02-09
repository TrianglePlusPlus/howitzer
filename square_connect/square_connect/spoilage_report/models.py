from django.db import models
# Importing models from other apps
from app.models import Service
from data.transaction import LocationsRequest, PaymentRequest, format_money

class SpoilageReport(models.Model):
    # TODO
    date = models.DateField()
    service = models.ForeignKey("app.Service")
    
    def add_items_from_json_data(self, json_data):
        # TODO: Test this
        for transaction in json_data:
            for item in transaction['itemizations']:
                try:
                    spoiled = False
                    for discount in item['discounts']:
                        if discount['name'] == 'Spoil': spoiled = True
                    if spoiled:
                        spoiled_item = SpoilageItem()
                        spoiled_item.report_id=self.id
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
                        spoiled_item.quantity = int(item['quantity'])
                        spoiled_item.save()
                except IndexError:
                    # There's nothing to do
                    pass

    def get_report(self, report_id):
        return SpoilageReport.objects.get(id=report_id)
        
    @property
    def get_associated_items(self):
        return SpoilageItem.objects.filter(pk=self.id)

    @staticmethod
    def search_reports(start_date, end_date, service=None):
        if service is not None:
            return SpoilageReport.objects.filter(date__range=(start_date, end_date), service__name=service)
        else:
            SpoilageReport.objects.filter(date__range=(start_date, end_date))


class SpoilageItem(models.Model):
    """ A single spoiled item
    Part of a spoilage report """
    name = models.CharField(max_length=50, default='') 
    variant = models.CharField(max_length=100, default='')
    sku = models.CharField(max_length=12, default='') 
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    quantity = models.IntegerField(default=1)
    # The report is the SpoilageReport which the item belongs to
    report = models.ForeignKey('SpoilageReport')
