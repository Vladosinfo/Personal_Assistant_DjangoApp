from django import forms
from .models import Contact


class DaysAheadForm(forms.Form):
    days_ahead = forms.IntegerField(
        label='Days Ahead',
        min_value=1,
        initial=7,
        required=True,
        help_text='Enter the number of days ahead to check for upcoming birthdays.'
    )


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
    birthday = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Contact
        fields = ['name', 'surname', 'email', 'phone', 'birthday', 'address']
