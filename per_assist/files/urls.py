from django.urls import path
from . import views

app_name = 'files'

urlpatterns = [
    path('', views.file_list, name='file_list'),
    path('upload/', views.upload_file, name='upload_file'),
    path('files/download/<int:file_id>/', views.download_file, name='download_file'),
    path('files/view/<int:file_id>/', views.view_file, name='view_file'),
    path('files/delete/<int:file_id>/', views.delete_file, name='delete_file'),
]
