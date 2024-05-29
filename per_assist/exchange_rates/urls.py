from django.urls import path, re_path
from . import views

app_name = 'exchange_rates'

urlpatterns = [
    path('exchange_rate/', views.exchange_rate, name='exchange_rate'),
    path('', views.exchange_rates, name='exchange_rates'),
    path('delete/<int:rate_id>', views.delete_rate, name='delete'),
]
