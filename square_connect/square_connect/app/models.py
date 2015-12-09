from django.db import models
from data.transaction import LocationsRequest

class Service(models.Model):
    name = models.CharField(max_length=40)
    merchant_id = models.CharField(max_length=13)

    @staticmethod
    def regenerate_services():
        # TODO
        locations = LocationsRequest.auto()
        for location, store_merchant_id in locations.items():
            Service.objects.create(name=location, merchant_id=store_merchant_id)