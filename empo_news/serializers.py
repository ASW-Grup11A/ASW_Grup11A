from rest_framework import serializers

from empo_news.models import UserFields, Contribution, Comment


class UserFieldsSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    date_joined = serializers.ReadOnlyField(source='user.date_joined')

    class Meta:
        model = UserFields
        fields = ['username', 'date_joined', 'karma', 'about', 'showdead', 'noprocrast', 'maxvisit',
                  'minaway', 'delay']


class ContributionSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    points = serializers.ReadOnlyField()
    publication_time = serializers.ReadOnlyField()
    comments = serializers.ReadOnlyField()
    liked = serializers.ReadOnlyField()
    show = serializers.ReadOnlyField()

    class Meta:
        model = Contribution
        fields = ['id', 'title', 'points', 'publication_time', 'url', 'text', 'comments',
                  'liked', 'show', 'user', 'hidden']


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    contribution = serializers.ReadOnlyField(source='contribution.id')
    parent = serializers.ReadOnlyField(source='parent.id')

    class Meta:
        model = Comment
        fields = ['id', 'points', 'publication_time', 'text', 'hidden', 'comments',
                  'liked', 'show', 'user', 'contribution', 'parent']


class UrlContributionSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    points = serializers.ReadOnlyField()
    publication_time = serializers.ReadOnlyField()
    comments = serializers.ReadOnlyField()
    liked = serializers.ReadOnlyField()
    show = serializers.ReadOnlyField()
    text = serializers.ReadOnlyField()

    class Meta:
        model = Contribution
        fields = ['id', 'title', 'points', 'publication_time', 'url', 'text', 'comments',
                  'liked', 'show', 'user']

class AskContributionSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    points = serializers.ReadOnlyField()
    publication_time = serializers.ReadOnlyField()
    comments = serializers.ReadOnlyField()
    liked = serializers.ReadOnlyField()
    show = serializers.ReadOnlyField()
    url = serializers.ReadOnlyField()

    class Meta:
        model = Contribution
        fields = ['id', 'title', 'points', 'publication_time', 'url', 'text', 'comments',
                  'liked', 'show', 'user']
