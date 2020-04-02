from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('empo_news.urls')),
    path('admin/', admin.site.urls),
    url('^auth', include('social_django.urls', namespace='social')),
]
