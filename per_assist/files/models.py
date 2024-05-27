from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import os


def validate_file_size(value):
    filesize = value.size
    if filesize > 10_000_000:
        raise ValidationError('Maximum file size 10 MB')
    return value


class File(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    file = models.FileField(upload_to='files/',
                            validators=[validate_file_size])

    category = models.CharField(max_length=50)

    @property
    def is_image(self):
        return self.file.name.lower().endswith(('.png',
                                                '.jpg',
                                                '.jpeg',
                                                '.gif',
                                                '.jfif'))

    @property
    def icon(self):
        _, extension = os.path.splitext(self.file.name)
        extension = extension.lower()[1:]
        icon_dict = {
            'txt': 'txt_icon.png',
            'pdf': 'pdf_icon.png',
            'doc': 'doc_icon.png',
            'docx': 'doc_icon.png',
            'xls': 'xls_icon.png',
        }
        return icon_dict.get(extension, 'default_icon.png')
