from django.forms import ModelForm, CharField
from .models import Weather


class WeatherForm(ModelForm):
    cur_day = CharField(min_length=3, max_length=50, required=True)
    min_temperature = CharField(min_length=3, max_length=50, required=True)
    max_temperature = CharField(min_length=3, max_length=50, required=True)
    class Meta:
        model = Weather
        fields = ['cur_day', 'min_temperature', 'max_temperature']
