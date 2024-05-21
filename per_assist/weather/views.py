from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Weather
from .scrapy import QuotesSpider, DataPipline

# Create your views here.
@login_required
def weather_list(request):

    return render(request, 'weather/weather_list.html')


def weather(request, cur_date=None):
    # if request.GET.get('cur_date') != None:
    cur_date = QuotesSpider.objects.get(id=request.GET.get('cur_date'))
        # notes = Note.objects.filter(tags=tag, user=request.user)
    # else:
    #     notes = Weather.objects.filter(user=request.user)

