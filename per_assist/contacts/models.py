from django.db import models
from django.contrib.auth.models import User
from .manager.contact_manager import ContactManager


class Contact(models.Model):
    name = models.CharField(max_length=50, null=False)
    surname = models.CharField(max_length=50, null=False)
    email = models.EmailField(max_length=250, null=False, unique=True)
    phone = models.CharField(max_length=20, null=False)
    birthday = models.DateField(null=False)
    address = models.CharField(max_length=250, null=True)
    additional = models.CharField(max_length=1100, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    objects = ContactManager()

    def __str__(self):
        return f"{self.name} {self.surname}"
