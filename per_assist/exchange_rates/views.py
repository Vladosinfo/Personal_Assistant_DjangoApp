import requests
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Exchange_rates
from .forms import ExchangeRatesForm
from django.conf import settings
from datetime import datetime
from .classes.Json_format import Json_format
from datetime import datetime, timedelta
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required
def exchange_rate(request):
    date = cur_date_get_from_db()
    exchange_rates = Exchange_rates.objects.filter(date=date)

    # If doesn't have rages for current data in db yet
    if len(exchange_rates) == 0:       
        exchange_rates = import_exchange_rates(request)
        # Rates has been imported and saved to db and we cat get them fore there
        if exchange_rates != False:
            exchange_rates = Exchange_rates.objects.filter(date=date)
            exchange_rates = json_to_dict(exchange_rates)
        else:
            # Rages hasn't been received and we will got rates from db day before
            date = cur_date_get_from_db(1)
            exchange_rates = Exchange_rates.objects.filter(date=date)
            # If rates table is empty
            if len(exchange_rates) == 0:
                date = cur_date_export_rates(1)
                exchange_rates = import_exchange_rates(request, 0, date)
                date = cur_date_get_from_db(1)
                exchange_rates = Exchange_rates.objects.filter(date=date)
            exchange_rates = json_to_dict(exchange_rates)
    else:
        exchange_rates = json_to_dict(exchange_rates)

    return render(request, 'exchange_rates/exchange_rates.html', {"date": exchange_rates['date'], "rates": exchange_rates['rates']})


@login_required
def exchange_rates(request):
    request_path = request.path
    list_rates = []
    if request.method == 'POST':
        form = ExchangeRatesForm(request.POST)
        if form.is_valid():
            list_rates = import_exchange_rates(request, form.cleaned_data['days'], form.cleaned_data['date'])
    else:
        # Output data from db
        form = ExchangeRatesForm()
        exchange_rates = Exchange_rates.objects.all().order_by('-date')
        list_rates = list_json_to_list_dict(exchange_rates)

        # Pagination
        paginator = Paginator(list_rates, 10)
        page_number = request.GET.get('page')
        try:
            list_rates = paginator.page(page_number)
        except PageNotAnInteger:
            list_rates = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            list_rates = paginator.page(paginator.num_pages)        

    return render(request, 'exchange_rates/exchange_rates.html', {'form': form, 'request_path': request_path, 'list_rates': list_rates})


def list_json_to_list_dict(list_json):
    list_dict_rates = []
    for item in list_json:
        dict_day = json_to_dict(item, False)
        list_dict_rates.append(dict_day)
    return list_dict_rates


def json_to_dict(json_str, inside_list=True):
    dict = {}
    if inside_list == True:
        dict['date'] = json_str[0].date.strftime("%Y-%m-%d")
        dict['rates'] = json.loads(json_str[0].rates)
    else:
        dict['date'] = json_str.date.strftime("%Y-%m-%d")
        dict['rates'] = json.loads(json_str.rates)
    
    return dict


def get_rate(url):
    response = requests.get(url)
    data = response.json()
    json_format = Json_format(data)
    course = json_format.generate()

    return course


@login_required
def save_to_db(request, rate):
    Exchange_rates.objects.create(date=rate["date"], rates=json.dumps(rate["exchangeRateList"]), user=request.user)


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
def import_exchange_rates(request, count = 0, get_date = False):
    ex_change_url_template = settings.EX_CHANGE_URL_TEMPLATE

    count = int(count)
    cur_date = cur_date_export_rates()
    if count > 1:
        list_rates = []
        for i in range(0, count+1):
            for_days_interval = timedelta(days=i)
            date_before_for_days_for_db_checking = (get_date - for_days_interval).strftime("%Y-%m-%d")
            res =  Exchange_rates.objects.filter(date=date_before_for_days_for_db_checking)
            if len(res) == 0:
                date_before_for_days_ = (get_date - for_days_interval).strftime("%d.%m.%Y")
                url = ex_change_url_template + date_before_for_days_
                response_rate = get_rate(url)
                if len(response_rate['exchangeRateList']) > 0:
                    save_to_db(request, response_rate)   
                    exchange_rates = Exchange_rates.objects.filter(date=date_before_for_days_for_db_checking)
                    dict_day = json_to_dict(exchange_rates)             
                    list_rates.append(dict_day)
            else:
                exchange_rates = Exchange_rates.objects.filter(date=date_before_for_days_for_db_checking)
                dict_day = json_to_dict(exchange_rates)             
                list_rates.append(dict_day)
                continue
        return  list_rates
    else:
        if get_date == False:
            url = ex_change_url_template + cur_date
        else:
            url = ex_change_url_template + get_date     

        response_rate = get_rate(url)

        if len(response_rate['exchangeRateList']) > 0:
            save_to_db(request, response_rate)
            response_rate = response_rate
        else:
            response_rate = False

    return response_rate    
