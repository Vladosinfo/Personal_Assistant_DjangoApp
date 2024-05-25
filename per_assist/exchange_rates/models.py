from django.db import models
from django.contrib.auth.models import User

class Exchange_rates(models.Model):
    date = models.DateField(null=False)   
    rates = models.CharField(max_length=350, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"{self.date} {self.rates}"