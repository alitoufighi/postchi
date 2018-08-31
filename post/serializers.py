from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from post.models import Post


class PostSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True, default=CurrentUserDefault())

    class Meta:
        model = Post
        fields = ('id', 'text', 'author', 'channel')
