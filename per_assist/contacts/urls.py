from django.urls import path
from . import views

app_name = 'contacts'

urlpatterns = [
    path('', views.main, name='main'),
    # path('tag/', views.tag, name='tag'),
    # path('author/', views.author, name='author'),
    # path('quote/', views.quote, name='quote'),
    # path('detail/<int:quote_id>', views.detail, name='detail'),
    # path('author_detail/<int:author_id>', views.author_detail, name='author_detail'),
    # path('delete/<int:quote_id>', views.delete_quote, name='delete'),
    # path('scrapy/', views.scrapy, name='scrapy'),
    # path('scrapyng_quotes/', views.scrapyng_quotes, name='scrapyng_quotes'),
    # # path('', views.main, name='main'),
    # # re_path('', views.main, name='main'),
    path('birthdays/', views.contacts_with_upcoming_birthdays, name='contacts_with_upcoming_birthdays'),
    path('search/', views.search_contacts, name='search_contacts'),
    path('add/', views.add_contact, name='add_contact'),
    path('edit/<int:pk>/', views.edit_contact, name='edit_contact'),
    path('delete/<int:pk>/', views.delete_contact, name='delete_contact'),
]
