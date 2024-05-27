import requests
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Exchange_rates
from django.conf import settings
from datetime import datetime
# from .classes.Client import Client
# from .classes.Request_rates import Request_rates
from .classes.Json_format import Json_format
from datetime import datetime, timedelta


@login_required
def exchange_rates(request):
    # date = cur_date_get_from_db(1)
    date = cur_date_get_from_db(1)
    # print(f"date555555555555555555: {date}")
    exchange_rates = Exchange_rates.objects.filter(date=date)

    # print(f"exchange_rates 1111111111111111111: {exchange_rates[0].rates}")

    if len(exchange_rates) == 0:
        exchange_rates = import_exchange_rates(request)
        # exchange_rates = json_to_dict(exchange_rates)   # TODO
        # print(f"exchange_rates: {exchange_rates}")
    else:
        exchange_rates = json_to_dict(exchange_rates)

    return render(request, 'exchange_rates/exchange_rates.html', {"date": exchange_rates['date'], "rates": exchange_rates['rates']})


def json_to_dict(json_str):
    dict = {}
    dict['date'] = json_str[0].date.strftime("%Y-%m-%d")
    dict['rates'] = json.loads(json_str[0].rates)

    # print(f"dict 222222222222222222222222: {dict}")

    return dict


def get_rate(url):
    response = requests.get(url)
    data = response.json()
    # print(f"data 55555555555555555555555: {data}")
    json_format = Json_format(data)
    # print(f"json_format 7777777777777777777777: {json_format}")
    course = json_format.generate()

    return course


@login_required
def save_to_db(request, rate):
    Exchange_rates.objects.create(date=rate["date"], rates=json.dumps(rate["exchangeRateList"]), user=request.user)

    # print(f"rate :77777777777777777: {rate}")


def cur_date_export_rates(day=0):
    cur_date = datetime.now()
    if day == 0:
        current_data = cur_date.strftime("%d.%m.%Y")
    else:
        for_days_interval = timedelta(day)
        current_data = (cur_date - for_days_interval).strftime("%d.%m.%Y")
    return current_data


def cur_date_get_from_db(day=0):
    cur_date = datetime.now()
    if day == 0:
        current_data = cur_date.strftime("%Y-%m-%d")
    else:
        for_days_interval = timedelta(day)
        current_data = (cur_date - for_days_interval).strftime("%Y-%m-%d")

    return current_data


@login_required
def import_exchange_rates(request, count = 0):
    ex_change_url_template = settings.EX_CHANGE_URL_TEMPLATE

    count = int(count)
    # cur_date = datetime.now()
    # cur_date = '26.05.2024'
    cur_date = cur_date_export_rates()
    if count > 1:
        for i in range(1, count):
            for_days_interval = timedelta(days=i)
            date_before_for_days_ = (cur_date - for_days_interval).strftime("%d.%m.%Y")
            print(f"reading rages for date: {date_before_for_days_}")
            url = ex_change_url_template + date_before_for_days_
            response_rate = get_rate(url)
    else:
        # current_datetime = datetime.now().strftime("%d.%m.%Y")
        # url = ex_change_url_template + current_datetime
        url = ex_change_url_template + cur_date
        
        print(f"reading rages for date: {cur_date}")

        response_rate = get_rate(url)
        # print(f"response_rate7777777777777: {response_rate}")
        # save_to_db(request, response_rate)


    return response_rate    

    # return render(request, 'exchange_rates/exchange_rates.html', {"exchange_rates": exchange_rates })
