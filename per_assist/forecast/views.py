import requests
from django.shortcuts import render
from django.conf import settings
# from django.http import JsonResponse
from .models import Weather


def get_weather(request):
    api_key = settings.API_KEY_WEATHER
    location = request.GET.get('location', 'Kyiv')
    url = f'http://api.weatherstack.com/current?access_key={api_key}&query={location}'

    response = requests.get(url)
    data = response.json()

    weather_data = data.get('current', {})
    weather = Weather(
        location=location,
        temperature=weather_data.get('temperature', 0),
        description=weather_data.get('weather_descriptions', [''])[0]
    )
    weather.save()

    return render(request, 'weather_forecast.html', {'weather': weather})
