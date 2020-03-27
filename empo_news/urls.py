from django.urls import path

from . import views

app_name = 'empo_news'
urlpatterns = [
    path('', views.index, name='index'),
    path('submit/', views.submit, name='submit'),
]
