from django.db import models

class MailingList(models.Model):
    """ A collection of Persons
    Emails are sent to all members of a MailingList """
    def __str__(self):
        return '%s mailing list' % self.service

    service = models.ForeignKey("app.Service")

    @property
    def members(self):
        return Person.objects.filter(mailing_list=self)

class PersonManager(models.Manager):
    def create_person(self, mailing_list, first_name, last_name, email):
        person = self.create(mailing_list=mailing_list, first_name=first_name, last_name=last_name, email=email)
        return person

class Person(models.Model):
    """ A single user
    Part of a mailing list """
    def __str__(self):
        return self.first_name + ' ' + self.last_name

    mailing_list = models.ForeignKey("mailer.MailingList")
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()

    objects = PersonManager()


