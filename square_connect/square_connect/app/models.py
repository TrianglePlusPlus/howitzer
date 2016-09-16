from django.db import models
from data.connect import LocationsRequest

class Service(models.Model):
    name = models.CharField(max_length=40)
    merchant_id = models.CharField(max_length=13)

    @staticmethod
    def regenerate_services():
        """ Populates the database with services and merchant ids
        If a service is not found in the database it is entered
        If a merchant id was changed on Square's side then it is updated
        """
        locations = LocationsRequest.auto()
        active_locations = Service.objects.all()
        # Add locations based on name
        for location, store_merchant_id in locations.items():
            location_found = False
            for entry in active_locations:
                if entry.name == location:
                    location_found = True
            if not location_found:
                Service.objects.create(name=location, merchant_id=store_merchant_id)
        # Update merchant ids if they are outdated
        for location, store_merchant_id in locations.items():
            merchant_id_found = False
            for entry in active_locations:
                if entry.merchant_id == store_merchant_id:
                    merchant_id_found = True
            if not merchant_id_found:
                storefront = Service.objects.get(name=location)
                storefront.merchant_id = store_merchant_id
                storefront.save()