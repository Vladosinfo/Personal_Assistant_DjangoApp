from django.urls import path, re_path
from . import views

app_name = 'notes'

urlpatterns = [
    # path('', views.main, name='main'),
    path('', views.notes, name='notes'),
    path('tag/', views.tag, name='tag'),
    # path('author/', views.author, name='author'),
    path('note/', views.note, name='note'),
    path('notes/', views.notes, name='notes'),
    path('detail/<int:note_id>', views.detail, name='detail'),
    # path('author_detail/<int:author_id>', views.author_detail, name='author_detail'),
    path('delete/<int:note_id>', views.delete_note, name='delete'),
    path('update/<int:note_id>', views.update_note, name='update'),
    path('update_note/<int:note_id>', views.update_note, name='update_note'),
    path('tags/', views.tags, name='tags'),
    path('updatet/<int:tag_id>/', views.update_tag, name='updatet'),
    path('update_tag/<int:tag_id>/', views.update_tag, name='update_tag'),
    # path('scrapyng_quotes/', views.scrapyng_quotes, name='scrapyng_quotes'),
    # # path('', views.main, name='main'),
    # # re_path('', views.main, name='main'),
]
