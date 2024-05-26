from django.db import models


class Weather(models.Model):
    location = models.CharField(max_length=200)
    temperature = models.FloatField()
    description = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Weather for {self.location} at {self.timestamp}'
