import json
import psycopg2
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import WeatherForm
from .models import Weather
from .scrapyapp import DataPipline


# Create your views here.
@login_required
def weather_list(request):

    return render(request, 'weather/weather_list.html')


# def weather(request, id=None):
#     weather = DataPipline()
#     if request.GET.get('id') != None:
#         cur_date = Weather.objects.get(id=request.GET.get('id'))
#         max_temperature = Weather.max_temperature
#         min_temperature = Weather.min_temperature
#
#     return render(request, 'weather/forecast.html',
#                       {"cur_date": cur_date, "max_temperature": max_temperature, "min_temperature": min_temperature})


conn = psycopg2.connect(
        dbname='per_assist',
        user='postgres',
        password='changeme',
        host='127.0.0.1',
        port='5540'
    )
cur = conn.cursor()



with open('weather/weather.json', 'r', encoding='utf-8') as fd:
    data = json.load(fd)

# for item in data:
#     cur.execute(
#         "INSERT INTO weather_weather (cur_day, min_temperature, max_temperature) VALUES (%s, %s, %s)",
#         (item['cur_date'], item['min_temperature'], item['max_temperature'])
#
# )

conn.commit()

cur.close()
conn.close()
@login_required
def weather_get(request):
    weather_get = Weather.objects.filter(id=request.id).order_by('id')
    return render(request, 'weather/weather_list.html', {"weather_get": weather_get})
    # if request.method == 'POST':
    #     form = WeatherForm(request.POST)
    #     if form.is_valid():
    #         cur_day = form.save(commit=False)
    #         form.save()
    #         return redirect(to='contacts:main')
    #     else:
    #         return render(request, 'notes/tag.html', {'form': form})
    #
    # return render(request, 'notes/tag.html', {'form': TagForm()})
    # return render(request, 'notes/notes.html', {"notes": notes, "tag_size_block": tag_size_block, "most_used_tags": most_used_tags})
