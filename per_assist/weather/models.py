from django.db import models


class Weather(models.Model):
    cur_day = models.CharField(max_length=50, null=False, unique=True)
    min_temperature = models.CharField(max_length=50, null=False, unique=True)
    max_temperature = models.CharField(max_length=50, null=False, unique=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['cur_day', 'min_temperature', 'max_temperature'], name='weather')
        ]

    def __str__(self):
        return f"{self.cur_day}"