from django.urls import path
from . import views

app_name = 'the_news'

urlpatterns = [
    path('', views.news_list, name='news_list'),
    path('<int:pk>/', views.news_detail, name='news_detail'),
    # path('category/<str:category>/', views.news_category, name='news_category'),
    path('fetch-news/', views.fetch_news_view, name='fetch_news'),
]
