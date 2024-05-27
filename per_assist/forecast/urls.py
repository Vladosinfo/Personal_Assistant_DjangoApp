from django.urls import path
from . import views

app_name = 'forecast'

urlpatterns = [
    path('', views.get_weather_forecast, name='get_weather_forecast'),
    path('current/', views.get_current_weather, name='get_current_weather'),
]
