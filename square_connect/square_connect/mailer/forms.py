from django import forms
from django.conf import settings
from .models import Person, Subscription

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ('first_name', 'last_name', 'email')

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ('service', 'discount')
