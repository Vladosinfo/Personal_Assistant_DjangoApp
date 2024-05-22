from django.forms import ModelForm, CharField, TextInput, Textarea, ChoiceField, ModelChoiceField, Select, HiddenInput
from django import forms
from .models import Tag, Note


class TagForm(ModelForm):

    name = CharField(min_length=3, max_length=25, required=True, widget=TextInput())
    
    class Meta:
        model = Tag
        fields = ['name']


class NoteForm(ModelForm):
    title = CharField(min_length=5, max_length=70, required=True, widget=TextInput())  
    text = CharField(min_length=10, max_length=2500, required=True, widget=Textarea)  

    class Meta:
        model = Note
        # fields = ['note']
        # exclude = ['tags']
        fields = ['title', 'text']
        exclude = ['tags']


class UpdateNoteForm(ModelForm):
    title = CharField(min_length=5, max_length=70, required=True, widget=TextInput())  
    text = CharField(min_length=10, max_length=2500, required=True, widget=Textarea)  

    class Meta:
        model = Note
        fields = ['title', 'text', 'tags', 'user']


class NotesSearchForm(forms.Form):
    SEARCH_CHOICES = (
        ('title', 'Title'),
        ('text', 'Note')
    )

    find_note_criteria = forms.ChoiceField(label='Search by', choices=SEARCH_CHOICES)
    find_note_value = forms.CharField(label='Enter value')        