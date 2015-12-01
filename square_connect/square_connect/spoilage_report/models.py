from django.db import models
# Importing models from other apps
from square_connect.app.models import Service

class SpoilageReport(models.Model):
    # TODO
    date = models.DateField()
    service = models.ForeignKey("Service")
    # Gets the spoilage items from a Json report
    def getReport(self, report):

        # Runs through report to populate a list of spoiled items with relevant fields
        for item in report:
            if item['itemizations'][0]['discounts'][0]['name'] == 'Spoilage':

                spoiledItem = SpoilageItem()
                
                spoiledItem.name = report[item]['itemizations'][0]['name']
                spoiledItem.id = report[item]['itemizations'][0]['item_detail']['item_id']
                spoiledItem.sku = report[item]['itemizations'][0]['item_detail']['sku']
                spoiledItem.price = report[item]['itemizations'][0]['single_quantity_money']

                self.spoiledList.append(spoiledItem)

    def find_items(self):
        spoilage_items = SpoilageItem.objects.filter(pk=self.pk)

class SpoilageItem(models.Model):
    # TODO
<<<<<<< HEAD
    name = models.CharField(max_length=50) # Max length 50
    sku = models.CharField(max_length=12) # Max length 12
=======
    name = models.CharField(max_length=50)
    sku = models.CharField(max_length=12)
>>>>>>> parent of 67c3cb2... Shit is getting out of control
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.IntegerField()
    # The report is the SpoilageReport which the item belongs to
    report = models.ForeignKey('SpoilageReport')
