from django.shortcuts import render, redirect, get_object_or_404
from django.core.management import call_command
from .models import News
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def news_list(request):
    news = News.objects.all().order_by('-published_date')
    selected_category = request.GET.get('categories')
    request_path = request.path

    if selected_category and selected_category != '':
        news = news.filter(category__contains=selected_category).order_by('-published_date')

    # Pagination
    paginator = Paginator(news, 10)
    page_number = request.GET.get('page')
    try:
        news = paginator.page(page_number)
    except PageNotAnInteger:
        news = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        news = paginator.page(paginator.num_pages)

    return render(request, 'news/news_list.html',
                  {'news': news,
                   'selected_category': selected_category,
                   'request_path': request_path})


def news_detail(request, pk):
    news = get_object_or_404(News, pk=pk)
    return render(request, 'news/news_detail.html', {'news': news})


def main_news_list(request):
    news = News.objects.all().order_by('-published_date')
    news = news.filter(category='general').order_by('-published_date')
    return render(request, 'contacts/index.html', {'news': news})


def fetch_news_view(request):
    call_command('fetch_news')
    return redirect('the_news:news_list')
