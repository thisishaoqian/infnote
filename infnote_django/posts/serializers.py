from rest_framework import serializers

from utils.serializers import TimestampField, ObjectIdField
from users.serializers import UserField

from .models import *


class LastReplyField(serializers.RelatedField):
    def to_internal_value(self, data):
        pass

    def to_representation(self, value):
        if value:
            return PostBriefSerializer(Post.objects.get(transaction_id=value)).data
        else:
            return None


class PostSerializer(serializers.ModelSerializer):
    post_id = ObjectIdField(source='id', read_only=True, required=False)
    date_submitted = TimestampField(read_only=True, required=False)
    date_confirmed = TimestampField(read_only=True, required=False)
    reply_to = serializers.CharField(required=True, allow_null=True, allow_blank=False)
    last_reply = LastReplyField(read_only=True)
    user = UserField(read_only=True, source='public_address')

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
            'id', 'user',
            'views', 'replies', 'last_reply', 'base_to',
            'is_confirmed', 'block_height', 'public_address'
        )


class PostBriefSerializer(PostSerializer):

    class Meta(PostSerializer.Meta):
        exclude = None
        fields = ('post_id', 'title', 'date_submitted', 'last_reply', 'user', 'replies')
