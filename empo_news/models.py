
from django.db import models


class User(models.Model):
    username = models.CharField(max_length=15, primary_key=True)
    password = models.CharField(max_length=72)


class Contribution(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=2000)
    points = models.IntegerField(default=1)
    publication_time = models.DateTimeField('publication date')
    url = models.CharField(max_length=500, null=True)
    text = models.CharField(max_length=2000, null=True)

    def get_type(self):
        if self.url is not None:
            return "url"
        elif self.text is not None:
            return "ask"
        return "failure"
