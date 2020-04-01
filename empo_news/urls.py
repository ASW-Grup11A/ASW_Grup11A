from django.conf.urls import url
from django.urls import path, include

from . import views

app_name = 'empo_news'
urlpatterns = [
    path('submit/', views.submit, name='submit'),
    path('', views.main_page, name='main_page'),
    path('newest', views.new_page, name='new_page'),
    path('notimplemented', views.not_implemented, name='not_implemented'),
    path('user_page', views.profile, name='user_page'),
    #path('update', views.updateUserFields(), name='user_page_update'),
    url('', include('social.apps.django_app.urls', namespace='social')),
    path('logout', views.logout),
]
