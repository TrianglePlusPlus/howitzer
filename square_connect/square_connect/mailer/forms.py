from django import forms
from django.conf import settings
from .models import Person

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ('mailing_list', 'first_name', 'last_name', 'email')

class MailerPersonForm(PersonForm):
    discount = forms.ChoiceField(choices=settings.DISCOUNTS)

    class Meta(PersonForm.Meta):
        fields = PersonForm.Meta.fields + ('discount',)
