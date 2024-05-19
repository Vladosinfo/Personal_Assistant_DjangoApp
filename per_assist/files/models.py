from django.db import models
from django.contrib.auth.models import User


class File(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    file = models.FileField(upload_to='files/')
    category = models.CharField(max_length=50)
