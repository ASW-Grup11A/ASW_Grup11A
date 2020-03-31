from django.conf.urls import url
from django.urls import path, include

from asw_grup11a import settings
from . import views, admin

app_name = 'empo_news'
urlpatterns = [
    path('submit/', views.submit, name='submit'),
    path('', views.main_page, name='main_page'),
    path('newest', views.new_page, name='new_page'),
    path('notimplemented', views.not_implemented, name='not_implemented'),
    url('', include('social.apps.django_app.urls', namespace='social')),
]
