from rest_framework import serializers
from .models import *

from posts.models import Post
from posts.serializers import PostBriefSerializer


class LastTopicField(serializers.Field):
    def to_internal_value(self, data):
        pass

    def to_representation(self, value):
        post = Post.objects.filter(reply_to__isnull=True, category=value).order_by('-date_submitted').first()
        if post:
            return PostBriefSerializer(post).data
        return None


class CategroySerializer(serializers.ModelSerializer):
    last_topic = LastTopicField(read_only=True)

    class Meta:
        model = Category
        exclude = ('id',)
        read_only_field = ('id', 'posts', 'topics')
