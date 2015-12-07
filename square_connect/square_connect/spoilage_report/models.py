from django.db import models
# Importing models from other apps
from app.models import Service
from data.transaction import LocationsRequest, PaymentRequest

class SpoilageReport(models.Model):
    # TODO
    date = models.DateField()
    service = models.ForeignKey("app.Service")
    
    def add_items_from_json_data(self, json_data):
        for item in report:
            if item['itemizations'][0]['discounts'][0]['name'] == 'Spoilage':
                spoiled_item = SpoilageItem.objects.create()
                spoiled_item.name = report[item]['itemizations'][0]['name']
                spoiled_item.id = report[item]['itemizations'][0]['item_detail']['item_id']
                spoiled_item.sku = report[item]['itemizations'][0]['item_detail']['sku']
                spoiled_item.price = report[item]['itemizations'][0]['single_quantity_money']
                spoiled_item.save()
    
    def get_report(self, report):
        pass
                
    def find_associated_items(self):
        spoilage_items = SpoilageItem.objects.filter(pk=self.pk)
        # TODO

class SpoilageItem(models.Model):
    # TODO
    name = models.CharField(max_length=50) 
    sku = models.CharField(max_length=12) 
    name = models.CharField(max_length=50)
    sku = models.CharField(max_length=12)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.IntegerField()
    # The report is the SpoilageReport which the item belongs to
    report = models.ForeignKey('SpoilageReport')
