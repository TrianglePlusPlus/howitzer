from django.db import models

class Service(models.Model):
    name = models.CharField(max_length=40)
    merchant_id = models.CharField(max_length=13)