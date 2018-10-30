import json
import re

from ecdsa.keys import BadSignatureError
from rest_framework import serializers
from utils.serializers import TimestampField
from .models import User

from utils.signature import Key


class UserSerializer(serializers.ModelSerializer):
    date_created = TimestampField(read_only=True, required=False)
    signature = serializers.CharField()

    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ('date_created', 'is_confirmed', 'topics', 'replies')

    def validate(self, attrs):
        user_id = attrs.get('id')
        if not re.match('[a-zA-Z0-9_-]{1,30}', user_id):
            raise serializers.ValidationError('User ID can only be combined by characters, numbers, - and _.')

        data = dict(attrs)
        public_key = data.pop('public_key')
        signature = data.pop('signature')
        key = Key(public_key)
        json_data = json.JSONEncoder(separators=(',', ':'), sort_keys=True, ensure_ascii=False).encode(data)
        try:
            key.verify(signature, json_data)
        except BadSignatureError:
            raise serializers.ValidationError('Invalid signature.')

        return attrs


class UserBriefSerializer(UserSerializer):

    class Meta(UserSerializer.Meta):
        fields = ('id', 'nickname', 'avatar', 'bio')


class UserBlockchainSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = ('id', 'nickname', 'avatar', 'bio', 'date_created', 'signature', 'public_key', 'gender')


class UserField(serializers.RelatedField):
    def to_internal_value(self, data):
        pass

    def to_representation(self, value):
        return UserBriefSerializer(instance=User.objects.get(id=value)).data
