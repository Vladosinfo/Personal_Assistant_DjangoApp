from django.urls import path
from . import views

app_name = 'forecast'

urlpatterns = [
    path('', views.get_weather, name='get_weather'),
]
