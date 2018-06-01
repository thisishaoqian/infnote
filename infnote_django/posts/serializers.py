from rest_framework import serializers

from utils.serializers import TimestampField, ObjectIdField

from .models import *


class PostSerializer(serializers.ModelSerializer):
    post_id = ObjectIdField(source='id', read_only=True, required=False)
    date_submitted = TimestampField(read_only=True, required=False)
    date_confirmed = TimestampField(read_only=True, required=False)
    reply_to = serializers.CharField(required=True, allow_null=True, allow_blank=False)

    def validate(self, attrs):
        data = super().validate(attrs)
        reply_to = attrs.get('reply_to')
        title = attrs.get('title')
        if (not reply_to or len(reply_to) == 0) and (not title or len(title) == 0):
            raise serializers.ValidationError({'title': ['This field may not be blank when reply_to is blank.']})
        return data

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
