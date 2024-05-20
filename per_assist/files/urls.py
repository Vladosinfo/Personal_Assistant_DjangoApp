from django.urls import path
from . import views
# from django.conf import settings
# from django.conf.urls.static import static

app_name = 'files'

urlpatterns = [
    path('', views.file_list, name='file_list'),
    path('upload/', views.upload_file, name='upload_file'),
    path('files/', views.file_list, name='file_list'),
    path('files/<str:category>/', views.filter_files, name='filter_files'),
    path('files/download/<int:file_id>/', views.download_file, name='download_file'),
    path('files/view/<int:file_id>/', views.view_file, name='view_file'),
]
