from django import forms
from .models import Contact
from phonenumber_field.modelfields import PhoneNumberField

class DaysAheadForm(forms.Form):
    days_ahead = forms.IntegerField(
        label='Days Ahead',
        min_value=1,
        required=False,
        help_text='Enter the number of days ahead to check for upcoming birthdays.'
    )


class ContactSearchForm(forms.Form):
    SEARCH_CHOICES = (
        ('name', 'Name'),
        ('surname', 'Surname'),
        ('phone', 'Phone'),
        ('email', 'Email'),
    )

    find_contact_criteria = forms.ChoiceField(label='Search by', choices=SEARCH_CHOICES, required=False)
    find_contact_value = forms.CharField(label='Enter value', required=False)


class ContactForm(forms.ModelForm):
    birthday = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    phone =PhoneNumberField(region='UA')
    additional_phone = forms.CharField(label='Additional Phone', required=False)
    additional_info = forms.CharField(required=False)
    
    class Meta:
        model = Contact
        fields = ['name', 'surname', 'email', 'phone', 'birthday', 'address', 'additional_phone', 'additional_info']
