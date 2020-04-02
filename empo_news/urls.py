from django.urls import path

from . import views

app_name = 'empo_news'
urlpatterns = [
    path('submit', views.submit, name='submit'),
    path('', views.main_page, name='main_page'),
    path('newest', views.new_page, name='new_page'),
    path('item', views.item, name='item'),
    path('addcomment', views.addcomment, name='addcomment'),
    path('notimplemented', views.not_implemented, name='not_implemented')
]

