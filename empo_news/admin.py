from django.contrib import admin

from empo_news.models import User, Contribution, UrlContribution, AskContribution

admin.site.register(User)
admin.site.register(Contribution)
admin.site.register(UrlContribution)
admin.site.register(AskContribution)
