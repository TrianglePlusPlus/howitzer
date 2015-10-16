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
    pass
