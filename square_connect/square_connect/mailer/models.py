from django.db import models
from django.conf import settings

class MailingList(models.Model):
    """ A collection of Persons.
    Emails are sent to all members of a MailingList """
    def __str__(self):
        return '%s mailing list' % self.service

    service = models.ForeignKey('app.Service')

    @property
    def members(self):
        return Person.objects.filter(mailing_list=self)

class Person(models.Model):
    """ A single user.
    Has any number of subscriptions. """
    def __str__(self):
        return self.first_name + ' ' + self.last_name

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    subscriptions = models.ManyToManyField('mailer.Subscription')

class Subscription(models.Model):
    """ A subscription.
    Includes a service and a discount, either of which may be 'all'. """

    # TODO: should these be foreign keys (we could create a Discount model in app.models)
    # the reasons we haven't done this include:
    #  - we have uppercase names associated with each service
    #  - a bunch of arbitrary excludes for services
    #  - discount categories
    service = models.CharField(max_length=256, choices=settings.SERVICES, default='all')
    discount = models.CharField(max_length=256, choices=settings.DISCOUNTS, default='all')

    @property
    def service_name(self):
        return settings.SERVICE_NAMES[self.service]
