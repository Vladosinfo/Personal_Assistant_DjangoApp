from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import TagForm, NoteForm, UpdateNoteForm, NotesSearchForm
from .models import Tag, Note
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required
def notes(request, tag_id=None):
    notes = []
    form = NotesSearchForm()
    if request.GET.get('tag_id') != None:
        tag = Tag.objects.get(id=request.GET.get('tag_id'))
        notes = Note.objects.filter(tags=tag, user=request.user).order_by('-id')
    elif request.method == 'POST':
        form = NotesSearchForm(request.POST)
        if form.is_valid():

            search_criteria = form.cleaned_data['find_note_criteria']
            search_value = form.cleaned_data['find_note_value']

            if search_criteria == 'title':
                notes = Note.objects.filter(title__icontains=search_value)
            elif search_criteria == 'text':
                notes = Note.objects.filter(text__icontains=search_value)    
    else:
        notes = Note.objects.filter(user=request.user).order_by('-id')

    notes_with_snippet = []
    for note in notes:
        note_snippet = {
            'id': note.id,
            'title': note.title,
            'text': note.text[:110] + '...',
            'tags': note.tags.all(),
            'user': note.user
        }
        notes_with_snippet.append(note_snippet)

    tag_size_block = list(range(28, 8, -2))
    most_used_tags = get_most_used_tags(request)
    request_path = request.path

    notes = notes_with_snippet

    # Pagination
    paginator = Paginator(notes, 10)
    page_number = request.GET.get('page')
    try:
        notes = paginator.page(page_number)
    except PageNotAnInteger:
        notes = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        notes = paginator.page(paginator.num_pages)

    return render(request, 'notes/notes.html', {"notes": notes, "tag_size_block": tag_size_block, "most_used_tags": most_used_tags, "request_path": request_path, "form": form})


@login_required
def tags(request):
    tags = Tag.objects.filter(user=request.user).order_by('-id')
    return render(request, 'notes/tags.html', {"tags": tags })


@login_required
def tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.user = request.user
            form.save()
            return redirect(to='notes:tags')
        else:
            return render(request, 'notes/tag.html', {'form': form})

    return render(request, 'notes/tag.html', {'form': TagForm()})


def update_tag(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id, user=request.user)
    
    if request.method == 'POST':
        form = TagForm(request.POST, instance=tag)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.user = request.user
            form.save()
            return redirect(to='notes:tags')
        else:
            return render(request, 'notes/tags.html', {'form': form})
    else:
        form = TagForm(instance=tag)

    return render(request, 'notes/update_tag.html', {'tag': tag, 'form': form})


@login_required
def note(request):
    # tags = Tag.objects.all()
    tags = Tag.objects.filter(user=request.user)

    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            new_note = form.save(commit=False)
            new_note.user = request.user
            new_note.save()

            choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'))
            for tag in choice_tags.iterator():
                new_note.tags.add(tag)     

            return redirect(to='notes:notes')
        else:
            return render(request, 'notes/note.html', {"tags": tags, 'form': form})

    return render(request, 'notes/note.html', {"tags": tags, 'form': NoteForm()})


@login_required
def detail(request, note_id):
    note = get_object_or_404(Note, pk=note_id, user=request.user)
    # author = get_object_or_404(Author, pk=note.author_id)
    return render(request, 'notes/detail.html', {"note": note})


@login_required
def delete_note(request, note_id):
    Note.objects.filter(pk=note_id, user=request.user).delete()
    return redirect(to='notes:notes')


@login_required
def update_note(request, note_id=None):

    tags = Tag.objects.filter(user=request.user)
    note = get_object_or_404(Note, id=note_id, user=request.user)
    
    if request.method == 'POST':

        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            update_note = form.save(commit=False)
            update_note.user = request.user
            update_note.save()

            note.tags.clear()

            choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'))
            for tag in choice_tags.iterator():
                update_note.tags.add(tag)     

            return redirect(to='notes:notes')
    else:
        form = UpdateNoteForm(instance=note)

    return render(request, 'notes/update_note.html', {"tags": tags, "note": note, 'form': form})


def get_most_used_tags(request):
    most_used_tags = Tag.objects.filter(user=request.user).annotate(num_notes=Count('note')).order_by('-num_notes')[:10]
    return most_used_tags
