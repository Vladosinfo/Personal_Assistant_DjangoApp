from django.urls import path, re_path
from . import views

app_name = 'notes'

urlpatterns = [
    # path('', views.main, name='main'),
    # path('tag/', views.tag, name='tag'),
    # path('author/', views.author, name='author'),
    path('note/', views.note, name='note'),
    # path('detail/<int:quote_id>', views.detail, name='detail'),
    # path('author_detail/<int:author_id>', views.author_detail, name='author_detail'),
    # path('delete/<int:quote_id>', views.delete_quote, name='delete'),
    # path('scrapy/', views.scrapy, name='scrapy'),
    # path('scrapyng_quotes/', views.scrapyng_quotes, name='scrapyng_quotes'),
    # # path('', views.main, name='main'),
    # # re_path('', views.main, name='main'),
]
