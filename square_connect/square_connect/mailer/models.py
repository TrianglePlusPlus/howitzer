from django.db import models

class MailingList(models.Model):
    """ A collection of Persons
    Emails are sent to all members of a MailingList """
    service = models.ForeignKey("app.Service")

class Person(models.Model):
    """ A single user
    Part of a mailing list """
    mailing_list = models.CharField(max_length=30) # should be a list
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
