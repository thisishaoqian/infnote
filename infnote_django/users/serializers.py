from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from utils.serializers import TimestampField, ObjectIdField

from .models import User


class UserSerializer(serializers.ModelSerializer):
    # TODO: email 等字段的 validator
    # mongo_id = ObjectIdField(source='user_id', read_only=True, required=False)
    date_created = TimestampField(read_only=True, required=False)
    date_last_login = TimestampField(read_only=True, required=False)
    date_birthday = TimestampField(required=False)

    class Meta:
        model = User
        # exclude = ('id',)
        exclude = ()
        read_only_fields = ('user_id', 'date_created', 'is_activated', 'is_confirmed', 'topics', 'replies', 'likes')
        extra_kwargs = {'password': {'write_only': True}}


class UserBriefSerializer(UserSerializer):

    class Meta(UserSerializer.Meta):
        exclude = None
        fields = ('user_id', 'nickname', 'topics')


class UserField(serializers.RelatedField):
    def to_internal_value(self, data):
        pass

    def to_representation(self, value):
        pass
        # try:
        #     user = User.objects.get(public_address=value)
        #     return UserBriefSerializer(user).data
        # except ObjectDoesNotExist:
        #     return {
        #         'nickname': 'Anonymous',
        #         'public_address': value,
        #         'topics': '∞',
        #         'likes': '∞',
        #         'replies': '∞',
        #     }
