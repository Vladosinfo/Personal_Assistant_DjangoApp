from django.db import models


class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    url = models.URLField(max_length=200, blank=True)
    category = models.CharField(max_length=50)
    published_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title
