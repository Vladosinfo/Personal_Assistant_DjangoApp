from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=50, null=False, unique=True)

    def __str__(self):
        return f"{self.name}"


class Note(models.Model):
    title = models.CharField(max_length=70, null=False)
    text = models.CharField(max_length=2500, null=False)
    tags = models.ManyToManyField(Tag)
    user = models.IntegerField("user_id", null=False)

    def __str__(self):
        return f"{self.note}"

