from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Contact
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError


class ContactModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.contact = Contact.objects.create(
            name='John',
            surname='Doe',
            email='john@example.com',
            phone='+380501234567',
            birthday='1990-01-01',
            address='123 Main St',
            user=self.user
        )

    def test_contact_creation(self):
        contact = Contact.objects.get(email='john@example.com')
        self.assertEqual(contact.name, 'John')
        self.assertEqual(contact.surname, 'Doe')
        self.assertEqual(contact.phone, '+380501234567')
        self.assertEqual(contact.birthday, datetime.strptime('1990-01-01', '%Y-%m-%d').date())
        self.assertEqual(contact.address, '123 Main St')
        self.assertEqual(contact.user.username, 'testuser')

    def test_contact_str_method(self):
        contact = Contact.objects.get(email='john@example.com')
        self.assertEqual(str(contact), 'John Doe')

    def test_contact_invalid_email(self):
        contact = Contact(
            name='Jane',
            surname='Doe',
            email='invalid-email',
            phone='+380501234567',
            birthday='1990-01-01',
            user=self.user
        )
        with self.assertRaises(ValidationError):
            contact.full_clean()

    def test_contact_invalid_phone(self):
        contact = Contact(
            name='Jane',
            surname='Doe',
            email='jane@example.com',
            phone='invalid-phone',
            birthday='1990-01-01',
            user=self.user
        )
        with self.assertRaises(ValidationError):
            contact.full_clean()


class ContactViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.contact = Contact.objects.create(
            name='John',
            surname='Doe',
            email='john@example.com',
            phone='+380501234567',
            birthday=datetime.now().date() - timedelta(days=5),
            address='123 Main St',
            user=self.user
        )

    def test_contact_list_view(self):
        response = self.client.get(reverse('contacts:contact_book'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'John Doe')
        self.assertTemplateUsed(response, 'contacts/contacts.html')

    def test_contact_detail_view(self):
        response = self.client.get(reverse('contacts:contact_detail', args=[self.contact.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'John Doe')
        self.assertTemplateUsed(response, 'contacts/contact_detail.html')

    def test_add_contact_view(self):
        response = self.client.get(reverse('contacts:add_contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contacts/add_contact.html')

        response = self.client.post(reverse('contacts:add_contact'), {
            'name': 'Jane',
            'surname': 'Doe',
            'email': 'jane@example.com',
            'phone': '+380501234568',
            'birthday': '1992-01-01',
            'address': '456 Main St'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Contact.objects.filter(email='jane@example.com').exists())

    def test_edit_contact_view(self):
        response = self.client.get(reverse('contacts:edit_contact', args=[self.contact.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contacts/edit_contact.html')

        response = self.client.post(reverse('contacts:edit_contact', args=[self.contact.id]), {
            'name': 'John',
            'surname': 'Smith',
            'email': 'john@example.com',
            'phone': '+380501234567',
            'birthday': '1990-01-01',
            'address': '123 Main St'
        })
        self.assertEqual(response.status_code, 302)
        self.contact.refresh_from_db()
        self.assertEqual(self.contact.surname, 'Smith')


class ContactAdditionalInfoTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.contact = Contact.objects.create(
            name='John',
            surname='Doe',
            email='john@example.com',
            phone='+380501234567',
            birthday='1990-01-01',
            address='123 Main St',
            user=self.user
        )

    def test_additional_phone_and_info(self):
        response = self.client.post(reverse('contacts:edit_contact', args=[self.contact.id]), {
            'name': 'John',
            'surname': 'Doe',
            'email': 'john@example.com',
            'phone': '+380501234567',
            'birthday': '1990-01-01',
            'address': '123 Main St',
            'additional_phone': '+380501234568',
            'additional_info': 'Some additional info'
        })
        self.assertEqual(response.status_code, 302)

        self.contact.refresh_from_db()

        self.assertEqual(self.contact.additional_phone, '+380501234568')
        self.assertEqual(self.contact.additional_info, 'Some additional info')
