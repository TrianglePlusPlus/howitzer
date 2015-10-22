"""
Definition of models.
"""

from django.db import models

class SpoilageReport(models.Model):
    # TODO
    # This contains all of the SpoilageItems for a given day
    pass

class SpoilageItem(models.Model):
    # TODO
    # Need to figure out what this needs
    # I think it needs:
    #   - its own id
    #   - Item/product id
    #   - quantity, ie the number of this item that were spoiled on a given day

    # For example bagels or sandwiches
    category = models.CharField(max_length=50)

    # For example chocolate or cinnamon raison
    subcategory = models.CharField(max_length=50)

    # In case we need to be more specific 
    sku = models.CharField(max_length=50)

    # Price
    price = models.IntegerField()

    # Quantity
    quantity = models.IntegerField()

    pass
