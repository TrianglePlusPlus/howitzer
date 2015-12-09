from django.db import models
# Importing models from other apps
from app.models import Service
from data.transaction import LocationsRequest, PaymentRequest, format_money

class SpoilageReport(models.Model):
    # TODO
    date = models.DateField()
    service = models.ForeignKey("app.Service")
    
    def add_items_from_json_data(self, json_data):
        # TODO
        for item in json_data:
            try:
                if item['itemizations'][0]['discounts'][0]['name'] == 'Spoil':
                    spoiled_item = SpoilageItem.objects.create(report_id=self.id)
                    spoiled_item.name = item['itemizations'][0]['name']
                    try:
                        # 1 is an arbitrary cut off, typical variants are "Pumpkin"
                        # for a muffin for example
                        if len(item['itemizations'][0]['item_variation_name']) > 1:
                            spoiled_item.variant = item['itemizations'][0]['item_variation_name']
                    except:
                        spoiled_item.variant = ''
                    try:
                        # 2 is an arbitrary cut off, normal SKUs should be 12
                        if len(item['itemizations'][0]['item_detail']['sku']) > 2:
                            spoiled_item.sku = item['itemizations'][0]['item_detail']['sku']
                    except:
                        spoiled_item.sku = ''
                    spoiled_item.price = format_money(item['itemizations'][0]['single_quantity_money']['amount'])
                    spoiled_item.save()
            except IndexError:
                # Nothing to do
                pass

    def get_report(self, report_id):
        return SpoilageReport.objects.get(id=report_id)

    def get_associated_items(self):
        return SpoilageItem.objects.filter(pk=self.id)

class SpoilageItem(models.Model):
    name = models.CharField(max_length=50, default='') 
    variant = models.CharField(max_length=100, default='')
    sku = models.CharField(max_length=12, default='') 
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    quantity = models.IntegerField(default=1)
    # The report is the SpoilageReport which the item belongs to
    report = models.ForeignKey('SpoilageReport')
