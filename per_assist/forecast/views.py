import requests
from datetime import datetime
from django.shortcuts import render
from django.conf import settings
# from django.http import JsonResponse
from .models import Weather


# def get_weather(request):
#     api_key = settings.API_KEY_WEATHER
#     location = request.GET.get('location', 'Kyiv')
#     url = f'http://api.weatherstack.com/current?access_key={api_key}&query={location}'

#     response = requests.get(url)
#     data = response.json()

#     weather_data = data.get('current', {})
#     weather = Weather(
#         location=location,
#         temperature=weather_data.get('temperature', 0),
#         description=weather_data.get('weather_descriptions', [''])[0]
#     )
#     weather.save()

#     return render(request, 'weather_forecast.html', {'weather': weather})


weather_descriptions = {
    0: 'Clear sky',
    1: 'Mainly clear',
    2: 'Partly cloudy',
    3: 'Overcast',
    45: 'Fog',
    48: 'Depositing rime fog',
    51: 'Light drizzle',
    53: 'Moderate drizzle',
    55: 'Dense drizzle',
    56: 'Light freezing drizzle',
    57: 'Dense freezing drizzle',
    61: 'Slight rain',
    63: 'Moderate rain',
    65: 'Heavy rain',
    66: 'Light freezing rain',
    67: 'Heavy freezing rain',
    71: 'Slight snow fall',
    73: 'Moderate snow fall',
    75: 'Heavy snow fall',
    77: 'Snow grains',
    80: 'Slight rain showers',
    81: 'Moderate rain showers',
    82: 'Violent rain showers',
    85: 'Slight snow showers',
    86: 'Heavy snow showers',
    95: 'Thunderstorm',
    96: 'Thunderstorm with slight hail',
    99: 'Thunderstorm with heavy hail'
}


def get_weather_forecast(request):
    latitude = request.GET.get('latitude', '50.4501')
    longitude = request.GET.get('longitude', '30.5234')
    url = f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=temperature_2m_max,precipitation_sum,weathercode&timezone=Europe/Kiev'

    response = requests.get(url)
    data = response.json()

    forecast = data.get('daily', {})
    weather_forecast = []

    for i in range(len(forecast['time'])):
        date = forecast['time'][i]
        max_temp = forecast['temperature_2m_max'][i]
        weather_code = forecast['weathercode'][i]
        description = weather_descriptions.get(weather_code, 'Unknown')

        weather = Weather(
            location='Kyiv',
            temperature=max_temp,
            description=description,
            forecast_date=date
        )
        weather.save()
        weather_forecast.append(weather)

    return render(request, 'weather_forecast.html', {'weather_forecast': weather_forecast})


def get_current_weather(request):
    latitude = request.GET.get('latitude', '50.4501')
    longitude = request.GET.get('longitude', '30.5234')
    url = f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true'

    response = requests.get(url)
    data = response.json()

    current_weather = data.get('current_weather', {})
    temperature = current_weather.get('temperature', 0)
    weather_code = current_weather.get('weathercode', 0)
    description = weather_descriptions.get(weather_code, 'Unknown')

    weather = Weather(
        location='Kyiv',
        temperature=temperature,
        description=description,
        forecast_date=datetime.today().date()
    )
    weather.save()

    return render(request, 'current_weather.html', {'weather': weather})
