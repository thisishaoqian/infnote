from rest_framework import serializers

from utils.serializers import TimestampField, ObjectIdField

from .models import User


class UserSerializer(serializers.ModelSerializer):
    # TODO: email 等字段的 validator
    user_id = ObjectIdField(source='id', read_only=True, required=False)
    date_created = TimestampField(read_only=True, required=False)
    date_last_login = TimestampField(read_only=True, required=False)
    date_birthday = TimestampField(required=False)

    class Meta:
        model = User
        exclude = ('id',)
        read_only_fields = ('id', 'date_created', 'is_activated', 'is_confirmed', 'topics', 'replies', 'likes')
        extra_kwargs = {'password': {'write_only': True}}


class UserBriefSerializer(UserSerializer):

    class Meta(UserSerializer.Meta):
        exclude = None
        fields = ('user_id', 'nickname', 'topics')
