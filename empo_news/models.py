from django.contrib.auth.models import User
from django.db import models


class Contribution(models.Model):
    user = models.ForeignKey(User, related_name="user", on_delete=models.CASCADE)
    title = models.CharField(max_length=2000)
    points = models.IntegerField(default=1)
    publication_time = models.DateTimeField('publication date')
    url = models.CharField(max_length=500, blank=True, null=True)
    text = models.CharField(max_length=2000, blank=True, null=True)
    likes = models.ManyToManyField(User, related_name="likes", blank=True)
    comments = models.IntegerField(default=0)
    liked = models.BooleanField(default=True)
    show = models.BooleanField(default=True)

    def get_type(self):
        if self.url is not None:
            return "url"
        elif self.text is not None:
            return "ask"
        return "failure"

    def total_likes(self):
        return self.likes.count()

    def is_liked(self):
        return self.liked
