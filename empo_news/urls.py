from django.conf.urls import url
from django.urls import path, include

from . import views

app_name = 'empo_news'
urlpatterns = [
    path('submit/', views.submit, name='submit'),
    path('', views.main_page, name='main_page'),
    path('pg/<int:pg>', views.main_page_pg, name='main_page_pg'),
    path('newest', views.new_page, name='new_page'),
    path('newest/pg/<int:pg>', views.new_page_pg, name='new_page_pg'),
    path('item', views.item, name='item'),
    path('addcomment', views.addcomment, name='addcomment'),
    path('like/<str:view>/<int:pg>/<int:contribution_id>', views.likes, name='likes'),
    path('hide/<str:view>/<int:pg>/<int:contribution_id>', views.hide, name='hide'),
    path('notimplemented', views.not_implemented, name='not_implemented'),
    path('user_page', views.profile, name='user_page'),
    url('', include('social.apps.django_app.urls', namespace='social')),
    path('logout', views.logout),
]
