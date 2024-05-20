from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponse
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
            return redirect('files:file_list')
    else:
        form = FileUploadForm()
    return render(request, 'upload.html', {'form': form})


def file_list(request):
    files = File.objects.filter(user=request.user)
    return render(request, 'file_list.html', {'files': files})


def filter_files(request, category):
    files = File.objects.filter(user=request.user, category=category)
    return render(request, 'file_list.html', {'files': files})


def download_file(request, file_id):
    file = get_object_or_404(File, id=file_id)
    if file.user != request.user:
        return HttpResponseForbidden("You do not have access to this file.")

    with file.file.open('rb') as f:
        file_data = f.read()

    response = HttpResponse(file_data, content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{file.file.name}"'
    return response


def view_file(request, file_id):
    file = get_object_or_404(File, id=file_id)
    if file.user != request.user:
        return HttpResponseForbidden("You do not have access to this file.")
    file_url = file.file.url
    return redirect(file_url)
