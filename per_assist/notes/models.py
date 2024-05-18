from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
    name = models.CharField(max_length=50, null=False, unique=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name='tag of username')
        ]

    def __str__(self):
        return f"{self.name}"


class Note(models.Model):
    title = models.CharField(max_length=70, null=False)
    text = models.CharField(max_length=2500, null=False)
    tags = models.ManyToManyField(Tag)
    # user = models.IntegerField("user_id", null=False)
    user=models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"{self.title}"

