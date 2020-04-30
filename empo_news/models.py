from django.contrib.auth.models import User
from django.db import models


class UserFields(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    karma = models.IntegerField(default=1)
    about = models.CharField(max_length=2000)
    showdead = models.BooleanField(default=False)
    noprocrast = models.BooleanField(default=False)
    maxvisit = models.IntegerField(default=1)
    minaway = models.IntegerField(default=180)
    delay = models.IntegerField(default=0)
    api_key = models.CharField(max_length=20, default='')


class Contribution(models.Model):
    user = models.ForeignKey(User, related_name="contribution", on_delete=models.CASCADE)
    title = models.CharField(max_length=2000)
    points = models.IntegerField(default=1)
    publication_time = models.DateTimeField('publication date')
    url = models.CharField(max_length=500, blank=True, null=True)
    text = models.CharField(max_length=2000, blank=True, null=True)
    user_likes = models.ManyToManyField(User, related_name="likes", blank=True)
    likes = models.IntegerField(default=1)
    user_id_hidden = models.ManyToManyField(User, related_name="hide", blank=True)
    hidden = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    liked = models.BooleanField(default=True)
    show = models.BooleanField(default=True)

    def get_type(self):
        if self.url is not None:
            return "url"
        elif self.text is not None:
            return "ask"
        return "failure"

    def get_class(self):
        return self.__class__.__name__


    def total_likes(self):
        return self.user_likes.count()

    def total_hidden(self):
        return self.user_id_hidden.count()

    def is_liked(self):
        return self.liked

    def is_hidden(self):
        return not self.show


class Comment(Contribution):
    contribution = models.ForeignKey(Contribution, related_name="contrib", on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
