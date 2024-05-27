import requests
from datetime import datetime
from django.shortcuts import render
from .models import Weather
from .dict_folder.dictionaries import weather_descriptions, location_description


def get_weather_forecast(request):
    loc = request.GET.get('location', '50.4501,30.5234')
    latitude, longitude = loc.split(',')
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
        location = location_description.get(loc, 'Kyiv')

        weather = Weather(
            location=location,
            temperature=max_temp,
            description=description,
            forecast_date=date
        )
        weather.save()
        weather_forecast.append(weather)
        request_path = request.path

    return render(request, 'weather_forecast.html',
                  {'weather_forecast': weather_forecast,
                   'location': location,
                   'request_path': request_path})


def get_current_weather(request):
    loc = request.GET.get('location', '50.4501,30.5234')
    latitude, longitude = loc.split(',')
    url = f'https://api.open-meteo.com/v1/forecast?latitude={latitude}\
            &longitude={longitude}&current_weather=true'

    response = requests.get(url)
    data = response.json()

    current_weather = data.get('current_weather', {})
    temperature = current_weather.get('temperature', 0)
    weather_code = current_weather.get('weathercode', 0)
    description = weather_descriptions.get(weather_code, 'Unknown')
    location = location_description.get(loc, 'Kyiv')
    request_path = request.path

    weather = Weather(
        location=location,
        temperature=temperature,
        description=description,
        forecast_date=datetime.today().date()
    )
    weather.save()

    return render(request, 'current_weather.html',
                  {'weather': weather,
                   'location': location,
                   'request_path': request_path})
