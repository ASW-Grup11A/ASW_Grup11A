from rest_framework import serializers

from empo_news.models import UserFields, Contribution, Comment


class UserFieldsSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = UserFields
        fields = ['karma', 'about', 'showdead', 'noprocrast', 'maxvisit', 'minaway', 'delay', 'user']


class ContributionSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Contribution
        fields = ['id', 'title', 'points', 'publication_time', 'url', 'text', 'comments',
                  'liked', 'show', 'user']


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    contribution = serializers.ReadOnlyField(source='contribution.id')
    parent = serializers.ReadOnlyField(source='parent.id')

    class Meta:
        model = Comment
        fields = ['id', 'title', 'points', 'publication_time', 'url', 'text', 'likes', 'hidden', 'comments',
                  'liked', 'show', 'user', 'contribution', 'parent']
