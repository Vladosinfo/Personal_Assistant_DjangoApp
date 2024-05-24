from django.db import models
from django.contrib.auth.models import User
from .manager.contact_manager import ContactManager
from phonenumber_field.modelfields import PhoneNumberField

class Contact(models.Model):
    name = models.CharField(max_length=50, null=False)
    surname = models.CharField(max_length=50, null=False)
    email = models.EmailField(max_length=250, null=False, unique=True)
    phone = PhoneNumberField(null=False)
    birthday = models.DateField(null=False)
    address = models.CharField(max_length=250, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    objects = ContactManager()

    def __str__(self):
        return f"{self.name} {self.surname}"
