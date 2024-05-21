from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# from ..notes.models import Tag, Note

# Create your views here.
@login_required
def weather_list(request):

    return render(request, 'weather/weather_list.html')


# def notes(request, tag_id=None):
#     if request.GET.get('tag_id') != None:
#         tag = Tag.objects.get(id=request.GET.get('tag_id'))
#         notes = Note.objects.filter(tags=tag, user=request.user)
#     else:
#         notes = Note.objects.filter(user=request.user)

