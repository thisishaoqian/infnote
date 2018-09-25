import json
import re

from rest_framework import serializers
from utils.serializers import TimestampField
from .models import User, NonceToken

from utils.signature import Key


class UserSerializer(serializers.ModelSerializer):
    date_created = TimestampField(read_only=True, required=False)
    date_last_login = TimestampField(read_only=True, required=False)
    date_birthday = TimestampField(required=False)
    signature = serializers.CharField()

    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ('date_created', 'is_confirmed', 'topics', 'replies')

    def validate(self, attrs):
        user_id = attrs.get('id')
        if not re.match('[a-zA-Z0-9_-]{1,30}', user_id):
            raise serializers.ValidationError('User ID can only be combined by characters, numbers, - and _.')

        public_key = attrs.get('public_key')
        signature = attrs.get('signature')
        data = dict(attrs)
        del data['public_key']
        del data['signature']
        key = Key(public_key)
        json_data = json.JSONEncoder(separators=(',', ':'), sort_keys=True).encode(data)
        if not key.verify(signature, json_data):
            raise serializers.ValidationError('Signature is not valid.')

        return attrs


class UserBriefSerializer(UserSerializer):

    class Meta(UserSerializer.Meta):
        fields = ('id', 'nickname', 'avatar', 'bio')


class UserField(serializers.RelatedField):
    def to_internal_value(self, data):
        pass

    def to_representation(self, value):
        return UserBriefSerializer(instance=User.objects.get(id=value)).data


class NonceTokenSerializer(serializers.ModelSerializer):
    date_expired = TimestampField(read_only=True)

    class Meta:
        model = NonceToken
        exclude = ('id',)
        editable = False
