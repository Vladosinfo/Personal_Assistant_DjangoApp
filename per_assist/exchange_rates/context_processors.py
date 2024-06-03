import json
from .models import Exchange_rates
from datetime import datetime, timedelta

from datetime import datetime
from exchange_rates.views import get_rates


def shared_data(request):
    rate = get_exchange_rate()
    if len(rate) < 1:
        get_rates(request)
        rate = get_exchange_rate()

    return {
        'date': rate['date'],
        'rates': rate['rates'],
    }


def get_exchange_rate():
    date = cur_date_get_from_db()
    exchange_rates = Exchange_rates.objects.filter(date=date)
    if len(exchange_rates) == 0:
        date = cur_date_get_from_db(1)
        exchange_rates = Exchange_rates.objects.filter(date=date)
        if len(exchange_rates) > 0:
            exchange_rates = json_to_dict(exchange_rates)
    else:
            exchange_rates = json_to_dict(exchange_rates)

    return exchange_rates


def json_to_dict(json_str, inside_list=True):
    dict = {}
    if inside_list == True:
        dict['date'] = json_str[0].date.strftime("%Y-%m-%d")
        dict['rates'] = json.loads(json_str[0].rates)
    else:
        dict['date'] = json_str.date.strftime("%Y-%m-%d")
        dict['rates'] = json.loads(json_str.rates)
    
    return dict


def cur_date_get_from_db(day=0):
    cur_date = datetime.now()
    if day == 0:
        current_data = cur_date.strftime("%Y-%m-%d")
    else:
        for_days_interval = timedelta(day)
        current_data = (cur_date - for_days_interval).strftime("%Y-%m-%d")

    return current_data
