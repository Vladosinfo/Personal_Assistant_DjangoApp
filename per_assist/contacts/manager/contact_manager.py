from django.db import models
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
