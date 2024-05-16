from django.db import models


class Contact(models.Model):
    name = models.CharField(max_length=50, null=False)
    surname = models.CharField(max_length=50, null=False)
    email = models.EmailField(max_length=250, null=False, unique=True)
    phone = models.CharField(max_length=20, null=False)
    birthday = models.DateField(null=False)
    user_id = models.IntegerField("user_id", null=False)
    additional = models.CharField(max_length=1100, null=True)

    def __str__(self):
        return f"{self.contact}"
