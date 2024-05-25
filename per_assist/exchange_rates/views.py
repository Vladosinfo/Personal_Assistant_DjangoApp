from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Exchange_rates
from django.conf import settings
from datetime import datetime


@login_required
def exchange_rates(request):
    exchange_rates = Exchange_rates.objects.filter(user=request.user).order_by('-id')
    return render(request, 'exchange_rates/exchange_rates.html', {"exchange_rates": exchange_rates })


@login_required
def import_exchange_rates(request):

    cources = []
    ex_change_url_template = settings.EX_CHANGE_URL_TEMPLATE
    current_datetime = datetime.now().strftime("%d.%m.%Y")
    url = ex_change_url_template + current_datetime
      
    print(f"reading rages for date: {current_datetime}")

    # course = await get_rate(url)
    # cources.append(course)

    # count = int(count)
    # cur_date = datetime.now()
    # if count > 1:
    #     for i in range(1, count):
    #         for_days_interval = timedelta(days=i)
    #         date_before_for_days_ = (cur_date - for_days_interval).strftime("%d.%m.%Y")
    #         print(f"reading rages for date: {date_before_for_days_}")
    #         url = url_template + date_before_for_days_
    #         course = await get_rate(url)
    #         cources.append(course)

    # return cources    

    #===================

    # exchange_rates = Exchange_rates.objects.filter(user=request.user).order_by('-id')
    # return render(request, 'exchange_rates/exchange_rates.html', {"exchange_rates": exchange_rates })