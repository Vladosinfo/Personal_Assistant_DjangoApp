from django.db import models
from datetime import timedelta, date
from django.contrib.auth.models import User
from django.db.models import Q


class ContactManager(models.Manager):
    def get_birthdays_in_range(self, start_date, end_date):
        start_month = start_date.month
        start_day = start_date.day
        end_month = end_date.month
        end_day = end_date.day

        if start_month <= end_month:
            contacts = self.filter(
                (Q(birthday__month=start_month, birthday__day__gte=start_day) |
                 Q(birthday__month=end_month, birthday__day__lte=end_day))
            )
        else:
            contacts = self.filter(
                (Q(birthday__month=start_month, birthday__day__gte=start_day) |
                 Q(birthday__month=end_month, birthday__day__lte=end_day) |
                 Q(birthday__month__gt=start_month, birthday__month__lt=end_month))
            )

        return contacts


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
