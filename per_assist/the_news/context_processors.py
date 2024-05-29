from .models import News
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def shared_data(request):
    news_main_not_auth = News.objects.filter(category='general').order_by('-published_date')

    # Pagination
    paginator = Paginator(news_main_not_auth, 10)
    page_number = request.GET.get('page')
    try:
        news_main_not_auth = paginator.page(page_number)
    except PageNotAnInteger:
        news_main_not_auth = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        news_main_not_auth = paginator.page(paginator.num_pages)

    return {'news_main_not_auth': news_main_not_auth}
