"""
Definition of models.
"""

from django.db import models

class SpoilageReport(models.Model):
    # TODO
    # This contains all of the SpoilageItems for a given day


    spoiledList = []

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

    # TODO Convert to Hash table

    pass

class SpoilageItem(models.Model):
    # TODO
    # Need to figure out what this needs
    # I think it needs:
    #   - its own id
    #   - Item/product id
    #   - quantity, ie the number of this item that were spoiled on a given day

    # Name of 
    name = models.CharField(max_length=50)

    # Unique own id
    
    id = models.CharField(max_length=50)

    # In case we need to be more specific 
    sku = models.CharField(max_length=50)

    # Price
    price = models.IntegerField()

    # Quantity
    quantity = models.IntegerField()

    pass


