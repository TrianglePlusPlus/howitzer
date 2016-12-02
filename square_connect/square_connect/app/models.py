from django.db import models
from data.transaction import LocationsRequest

service_names = {
    "mug": "MUG",
    "vittles": "Vital Vittles",
    "snaxa": "Hoya Snaxa",
    "ug": "Uncommon Grounds",
    "midnight": "Midnight Mug",
    "hilltoss": "Hilltoss",
}

discounts = [
    ('all', 'All Discounts'),
    ('$1.50 Off', '$1.50 Off'),
    ('1.50 Off', '1.50 Off'),
    ('CREDITED Spoilage', 'CREDITED Spoilage'),
    ('Cup Reuse', 'Cup Reuse'),
    ('Espresso 10 Drinks Card', 'Espresso 10 Drinks Card'),
    ('Espresso Loyalty Card', 'Espresso Loyalty Card'),
    ('Expired', 'Expired'),
    ('Green Bag Discount', 'Green Bag Discount'),
    ('Lau Employee Appreciation', 'Lau Employee Appreciation'),
    ('Office Hours', 'Office Hours'),
    ('Shift Drink - Accounting', 'Shift Drink - Accounting'),
    ('Shift Drink - Catering', 'Shift Drink - Catering'),
    ('Shift Drink - Hilltoss', 'Shift Drink - Hilltoss'),
    ('Shift Drink - Hoya Snaxa', 'Shift Drink - Hoya Snaxa'),
    ('Shift Drink - ITM', 'Shift Drink - ITM'),
    ('Shift Drink - MUG', 'Shift Drink - MUG'),
    ('Shift Drink - Main Office', 'Shift Drink - Main Office'),
    ('Shift Drink - Midnight', 'Shift Drink - Midnight'),
    ('Shift Drink - UG', 'Shift Drink - UG'),
    ('Shift Drink - Vital Vittles', 'Shift Drink - Vital Vittles'),
    ('Sorry Card', 'Sorry Card'),
    ('Spoil', 'Spoil'),
    ('Use - Catering', 'Use - Catering'),
    ('Use - MUG', 'Use - MUG'),
    ('Use - Vittles', 'Use - Vittles'),
]

class Service(models.Model):
    def __str__(self):
        return self.name

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
