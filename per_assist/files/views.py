from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import FileUploadForm
from .models import File


@login_required
def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.user = request.user
            file.save()
            return redirect('file_list')
    else:
        form = FileUploadForm()
    return render(request, 'upload.html', {'form': form})


def file_list(request):
    files = File.objects.filter(user=request.user)
    return render(request, 'file_list.html', {'files': files})


def filter_files(request, category):
    files = File.objects.filter(user=request.user, category=category)
    return render(request, 'file_list.html', {'files': files})
