from django.urls import path

from . import views

app_name = 'empo_news'
urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('notimplemented', views.not_implemented, name='not_implemented')
]
