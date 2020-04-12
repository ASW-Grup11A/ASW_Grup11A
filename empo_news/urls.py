from django.conf.urls import url
from django.urls import path, include

from . import views

app_name = 'empo_news'
urlpatterns = [
    path('submit/', views.submit, name='submit'),
    path('', views.main_page, name='main_page'),
    path('newest', views.new_page, name='new_page'),
    path('submitted', views.submitted, name='submitted'),
    path('item', views.item, name='item'),
    path('addcomment', views.add_comment, name='addcomment'),
    path('reply', views.add_reply, name='addreply'),
    path('like/<str:view>/<int:pg>/<int:contribution_id>', views.likes, name='likes'),
    path('likesubmit/<str:view>/<str:id>/<int:pg>/<int:contribution_id>', views.likes_submit, name='likes_submit'),
    path('hide/<str:view>/<int:pg>/<int:contribution_id>', views.hide, name='hide'),
    path('notimplemented', views.not_implemented, name='not_implemented'),
    path('like_comment/<int:comment_id>/<str:username>', views.likes_comment, name='likes_comment'),
    path('like_reply/<int:contribution_id>/<int:comment_id>', views.likes_reply, name='likes_reply'),
    path('like_contribution/<int:contribution_id>', views.likes_contribution, name='likes_contribution'),
    path('user_page/<str:username>', views.profile, name='user_page'),
    url('', include('social.apps.django_app.urls', namespace='social')),
    path('logout', views.logout),
    path('threads/<str:username>', views.threads, name='threads'),
    path('delete_comment/<int:commentid>', views.delete_comment, name='delete_comment'),
    path('update_comment/<int:commentid>', views.update_comment, name='update_comment'),
    path('comments', views.comments, name='comments'),
]
