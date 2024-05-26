from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Exchange_rates
from django.conf import settings
from datetime import datetime
# from .classes.Client import Client
# from .classes.Request_rates import Request_rates
from .classes.Json_format import Json_format
from datetime import datetime, timedelta
import requests


@login_required
def exchange_rates(request):
    exchange_rates = Exchange_rates.objects.filter(user=request.user).order_by('-id')

    exchange_result = import_exchange_rates(request)
    print(f"exchange_result: {exchange_result}")

    return render(request, 'exchange_rates/exchange_rates.html', {"exchange_result": exchange_result })


def get_rate(url):
    # client = Client(Request_rates, url)
    # data = await client.get_data()

    response = requests.get(url)
    data = response.json()

    # print(f"data 55555555555555555555555: {data}")

    json_format = Json_format(data)

    # print(f"json_format 7777777777777777777777: {json_format}")

    course = json_format.generate()

    return course
    # return True


@login_required
def import_exchange_rates(request, count = 0):
    # import asyncio

    cources = []
    ex_change_url_template = settings.EX_CHANGE_URL_TEMPLATE
    current_datetime = datetime.now().strftime("%d.%m.%Y")
    url = ex_change_url_template + current_datetime
      
    print(f"reading rages for date: {current_datetime}")

    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    # course = loop.run_until_complete(get_rate(url))  
    # course = get_rate(url)
    # cources.append(course)

    response = get_rate(url)
    # cources.append(response.json())
    cources.append(response)

    count = int(count)
    cur_date = datetime.now()
    if count > 1:
        for i in range(1, count):
            for_days_interval = timedelta(days=i)
            date_before_for_days_ = (cur_date - for_days_interval).strftime("%d.%m.%Y")
            print(f"reading rages for date: {date_before_for_days_}")
            url = ex_change_url_template + date_before_for_days_
            course = get_rate(url)
            cources.append(course)

    # print(f"cources: {cources}")

    return cources    

    #===================

    # exchange_rates = Exchange_rates.objects.filter(user=request.user).order_by('-id')
    # return render(request, 'exchange_rates/exchange_rates.html', {"exchange_rates": exchange_rates })
