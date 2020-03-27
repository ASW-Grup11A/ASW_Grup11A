from django.db import models


class User(models.Model):
    username = models.CharField(max_length=15, primary_key=True)
    password = models.CharField(max_length=72)
    hidden = models.ManyToManyField('Contribution', related_name="hidden_contributions", blank=True)
    upvoted = models.ManyToManyField('Contribution', related_name="upvoted_contributions", blank=True)

    def str(self):
        return self.username


class Contribution(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=2000)
    points = models.IntegerField(default=1)
    publication_time = models.DateTimeField('publication date')
    url = models.CharField(max_length=500, blank=True, null=True)
    text = models.CharField(max_length=2000, blank=True, null=True)
    comments = models.IntegerField(default=0)

    def get_type(self):
        if self.url is not None:
            return "url"
        elif self.text is not None:
            return "ask"
        return "failure"
