from django.contrib import admin


from empo_news.models import Contribution, UserFields

admin.site.register(UserFields)
admin.site.register(Contribution)

