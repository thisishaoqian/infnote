from rest_framework import serializers

from utils.serializers import TimestampField, ObjectIdField

from .models import *


class PostSerializer(serializers.ModelSerializer):
    post_id = ObjectIdField(source='id', read_only=True, required=False)
    date_submitted = TimestampField(read_only=True, required=False)
    date_confirmed = TimestampField(read_only=True, required=False)

    class Meta:
        model = Post
        exclude = ('id',)
        read_only_fields = (
            'id', 'transaction_id', 'public_key',
            'views', 'replies', 'is_confirmed', 'block_height',
        )


class ContentlessPostSerializer(PostSerializer):

    class Meta(PostSerializer.Meta):
        exclude = ('id', 'content')
