from django.urls import path, re_path
from . import views

app_name = 'contacts'

urlpatterns = [
    path('', views.main, name='main'),
    # path('author/', views.author, name='author'),
    # path('detail/<int:quote_id>', views.detail, name='detail'),
    # path('delete/<int:quote_id>', views.delete_quote, name='delete'),
    # # path('', views.main, name='main'),
    # # re_path('', views.main, name='main'),
]
