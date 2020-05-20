from django.conf.urls import url
from django.urls import path, include

from . import views
from .views import ContributionsViewSet, ContributionsIdViewSet, VoteIdViewSet, UnVoteIdViewSet, HideIdViewSet, \
    UnHideIdViewSet, CommentViewSet, CommentIdViewSet, ContributionCommentViewSet, ProfilesViewSet, ProfilesIdViewSet

app_name = 'empo_news'

contributions_view = ContributionsViewSet.as_view({
    'get': 'get_actual',
    'post': 'create'
})

contributions_id_view = ContributionsIdViewSet.as_view({
    'get': 'get_actual',
    'delete': 'delete_actual',
    'put': 'update_actual'
})

vote_id_view = VoteIdViewSet.as_view({
    'put': 'vote'
})

unvote_id_view = UnVoteIdViewSet.as_view({
    'put': 'unvote'
})

hide_id_view = HideIdViewSet.as_view({
    'put': 'hide'
})

unhide_id_view = UnHideIdViewSet.as_view({
    'put': 'unhide'
})

comments_view = CommentViewSet.as_view({
    'get': 'get_actual'
})

comments_id_view = CommentIdViewSet.as_view({
    'get': 'get_actual'
})

contribution_comments_view = ContributionCommentViewSet.as_view({
    'get': 'get_actual',
    'post': 'create_comment'
})

profiles_id_args = ProfilesViewSet.as_view({
    'put': 'update_actual'
})

profiles_id_kwargs = ProfilesIdViewSet.as_view({
    'get': 'get_actual'
})

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
    path('hide/<str:view>/<int:contribution_id>', views.hide_no_page, name='hide_no_page'),
    path('unhide/<str:view>/<int:pg>/<int:contribution_id>/<int:userid>', views.unhide, name='unhide'),
    path('like_comment/<int:comment_id>/<str:username>', views.likes_comment, name='likes_comment'),
    path('like_reply/<int:contribution_id>/<int:comment_id>/<str:path>', views.likes_reply, name='likes_reply'),
    path('like_contribution/<int:contribution_id>', views.likes_contribution, name='likes_contribution'),
    path('user_page/<str:username>', views.profile, name='user_page'),
    url('', include('social.apps.django_app.urls', namespace='social')),
    path('logout', views.logout),
    path('threads/<str:username>', views.threads, name='threads'),
    path('comments', views.comments, name='comments'),
    path('ask_list', views.ask_list, name='ask_list'),
    path('show_list', views.show_list, name='show_list'),
    path('hidden/<int:userid>', views.hidden, name='hidden'),
    path('voted_submissions', views.voted_submissions, name='voted_submissions'),
    path('voted_comments', views.voted_comments, name='voted_comments'),
    path('collapse/<int:contribution_id>/<int:comment_id>', views.collapse, name='collapse'),

    path('api/v1/contributions', contributions_view, name='api_contributions'),
    path('api/v1/contribution/<int:id>', contributions_id_view, name='api_contributions_id'),
    path('api/v1/contribution/<int:id>/vote', vote_id_view, name='api_vote_id'),
    path('api/v1/contribution/<int:id>/unvote', unvote_id_view, name='api_unvote_id'),
    path('api/v1/contribution/<int:id>/hide', hide_id_view, name='api_hide_id'),
    path('api/v1/contribution/<int:id>/unhide', unhide_id_view, name='api_unhide_id'),
    path('api/v1/comments', comments_view, name='api_comments'),
    path('api/v1/comment/<int:commentId>', comments_id_view, name='api_id_comments'),
    path('api/v1/contribution/<int:id>/comments', contribution_comments_view, name='api_contribution_comments'),
    path('api/v1/profile', profiles_id_args, name='api_profiles_id_args'),
    path('api/v1/profile/<str:username>', profiles_id_kwargs, name='api_profiles_id_kwargs'),
]
