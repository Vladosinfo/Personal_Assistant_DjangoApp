from django.db import models
from django.db.models import Q, Func, Value, CharField
from datetime import datetime, timedelta


class MonthDay(Func):
    function = 'TO_CHAR'
    template = '%(function)s(%(expressions)s, \'MM-DD\')'
    output_field = CharField()


class ContactManager(models.Manager):
    def get_birthdays_in_days(self, days):
        # start_date = timezone.now().date()
        start_date = datetime.now().date()
        end_date = start_date + timedelta(days=days)
        start_str = start_date.strftime('%m-%d')
        end_str = end_date.strftime('%m-%d')

        contacts = self.annotate(
            month_day=MonthDay('birthday')
        )

        if start_str <= end_str:
            contacts = contacts.filter(
                month_day__gte=start_str, month_day__lte=end_str
            )
        else:
            contacts = contacts.filter(
                Q(month_day__gte=start_str) | Q(month_day__lte=end_str)
            )

        return contacts
