from django.forms import ModelForm, CharField, TextInput, TextField, Textarea
from .models import WeatherNews


class WeatherForm(ModelForm):
    # name = CharField(min_length=3, max_length=25, required=True, widget=TextInput())
    cur_day = CharField(min_length=3, max_length=50, required=True)
    min_temperature = CharField(min_length=3, max_length=50, required=True)
    max_temperature = CharField(min_length=3, max_length=50, required=True)
    class Meta:
        model = WeatherNews
        fields = ['cur_day', 'min_temperature', 'max_temperature']
