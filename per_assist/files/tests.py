from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import File


class FileUploadTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_upload_file_success(self):
        with open('your/path/to/file', 'rb') as file:
            response = self.client.post(reverse('files:upload_file'), {'file': file, 'category': 'Test Category'})
        self.assertEqual(response.status_code, 302)

        uploaded_file = File.objects.first()
        self.assertEqual(uploaded_file.user, self.user)
        self.assertEqual(uploaded_file.category, 'Test Category')

    def test_upload_file_exceeds_limit(self):
        # Prepare a file exceeding the size limit
        with open('your/path/to/file', 'rb') as file:
            response = self.client.post(reverse('files:upload_file'), {'file': file, 'category': 'Large File'})
        self.assertEqual(response.status_code, 200)

        self.assertFalse(File.objects.exists())
