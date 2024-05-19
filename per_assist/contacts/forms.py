from django import forms
from .models import Contact


class DateRangeForm(forms.Form):
    start_date = forms.DateField(label='Start Date', widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(label='End Date', widget=forms.DateInput(attrs={'type': 'date'}))


class ContactSearchForm(forms.Form):
    SEARCH_CHOICES = (
        ('name', 'Name'),
        ('surname', 'Surname'),
        ('phone', 'Phone'),
        ('email', 'Email'),
    )

    find_contact_criteria = forms.ChoiceField(label='Search by', choices=SEARCH_CHOICES)
    find_contact_value = forms.CharField(label='Enter value')


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'surname', 'email', 'phone', 'birthday', 'address', 'additional']

