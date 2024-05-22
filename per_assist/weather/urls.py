from django.urls import path
from . import views
# from django.conf import settings
# from django.conf.urls.static import static

app_name = 'weather'

urlpatterns = [
    path('', views.weather_list, name='weather_list'),
    path('weather/', views.weather_list, name='weather_list'),
    # path('weather/', views.notes, name='notes'),
]
