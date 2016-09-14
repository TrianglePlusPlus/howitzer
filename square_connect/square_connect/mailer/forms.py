from django import forms
from .models import Person

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ('mailing_list', 'first_name', 'last_name', 'email')
