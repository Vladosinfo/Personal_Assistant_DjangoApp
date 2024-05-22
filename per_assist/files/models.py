from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def validate_file_size(value):
    filesize = value.size

    if filesize > 10_000_000:
        raise ValidationError('Maximum file size 10 MB')
    return value


class File(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    file = models.FileField(upload_to='files/', validators=[validate_file_size])
    category = models.CharField(max_length=50)
