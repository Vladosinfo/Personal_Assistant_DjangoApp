from django import forms
from .models import Exchange_rates
from datetime import datetime


class ExchangeRatesForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    days = forms.IntegerField(
        label='Days ago',
        min_value=0,
        max_value=7,
        required=False,
        help_text='number of days to receive currency rates'
    )

    class Meta:
        model = Exchange_rates
        fields = ['date', 'days']
