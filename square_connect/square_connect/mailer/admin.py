from django.contrib import admin

from .models import MailingList, Person

admin.site.register(MailingList)
admin.site.register(Person)
