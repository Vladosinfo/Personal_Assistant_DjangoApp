from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Exchange_rates


@login_required
def exchange_rates(request):
    exchange_rates = Exchange_rates.objects.filter(user=request.user).order_by('-id')
    return render(request, 'exchange_rates/exchange_rates.html', {"exchange_rates": exchange_rates })