# tests.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Note, Tag

class NoteTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.tag1 = Tag.objects.create(name='Tag1', user=self.user)
        self.tag2 = Tag.objects.create(name='Tag2', user=self.user)
        self.note = Note.objects.create(
            title='Test Note',
            text='This is a test note.',
            user=self.user
        )
        self.note.tags.add(self.tag1)

    def test_create_note(self):
        response = self.client.post(reverse('notes:note'), {
            'title': 'New Note',
            'text': 'This is a new note.',
            'tags': [self.tag1.id, self.tag2.id]
        })
        self.assertEqual(response.status_code, 302)

        note = Note.objects.get(title='New Note')
        self.assertEqual(note.text, 'This is a new note.')
        self.assertEqual(note.user, self.user)
        self.assertEqual(note.tags.count(), 0)

    def test_edit_note(self):
        response = self.client.post(reverse('notes:update_note', args=[self.note.id]), {
            'title': 'Updated Note',
            'text': 'This note has been updated.',
            'tags': [self.tag2.id]
        })
        self.assertEqual(response.status_code, 302)

        self.note.refresh_from_db()
        self.assertEqual(self.note.title, 'Updated Note')
        self.assertEqual(self.note.text, 'This note has been updated.')
        self.assertEqual(self.note.tags.count(), 0)
        self.assertNotIn(self.tag2, self.note.tags.all())


    def test_search_note_by_title(self):
        response = self.client.post(reverse('notes:notes'), {
            'find_note_criteria': 'title',
            'find_note_value': 'Test'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Note')

    def test_search_note_by_text(self):
        response = self.client.post(reverse('notes:notes'), {
            'find_note_criteria': 'text',
            'find_note_value': 'test note'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Note')

    def test_create_tag(self):
        response = self.client.post(reverse('notes:tag'), {
            'name': 'New Tag'
        })
        self.assertEqual(response.status_code, 302)

        tag = Tag.objects.get(name='New Tag')
        self.assertEqual(tag.user, self.user)

    def test_edit_tag(self):
        response = self.client.post(reverse('notes:update_tag', args=[self.tag1.id]), {
            'name': 'Updated Tag'
        })
        self.assertEqual(response.status_code, 302)

        self.tag1.refresh_from_db()
        self.assertEqual(self.tag1.name, 'Updated Tag')
