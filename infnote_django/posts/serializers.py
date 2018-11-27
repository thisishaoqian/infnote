import json

from ecdsa.keys import BadSignatureError
from rest_framework import serializers

from utils.serializers import TruncatedField
from utils.signature import Key
from users.serializers import UserField

from .models import *


class LastReplyField(serializers.RelatedField):
    def to_internal_value(self, data):
        pass

    def to_representation(self, value):
        if value:
            return PostBriefSerializer(Post.objects.get(payload_id=value)).data
        else:
            return None


class PostSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='payload_id', read_only=True)
    reply_to = serializers.CharField(required=False, allow_null=True, allow_blank=False)
    last_reply = LastReplyField(read_only=True)
    user = UserField(read_only=True, source='user_id')

    class Meta:
        model = Post
        exclude = ('payload_id',)
        read_only_fields = (
            'id', 'replies', 'last_reply', 'block_height', 'block_time', 'payload_id'
        )
        extra_kwargs = {'user_id': {'write_only': True}}

    def validate(self, attrs):
        reply_to = attrs.get('reply_to')
        title = attrs.get('title')
        if (not reply_to or len(reply_to) == 0) and (not title or len(title) == 0):
            raise serializers.ValidationError({'title': ['This field may not be blank when reply_to is blank.']})

        data = dict(self.initial_data)
        signature = data.pop('signature')
        user = User.objects.get(id=data.get('user_id'))
        key = Key(user.public_key)
        json_data = json.JSONEncoder(separators=(',', ':'), sort_keys=True, ensure_ascii=False).encode(data)
        try:
            key.verify(signature, json_data.encode('utf8'))
        except BadSignatureError:
            raise serializers.ValidationError('Invalid signature.')

        # if not attrs.get('id'):
        #     attrs['payload_id'] = base58.b58encode(hashlib.sha256(json_data.encode('utf8')).digest()).decode('ascii')
        # else:
        #     attrs['payload_id'] = attrs.get('id')

        return attrs


class PostBriefSerializer(PostSerializer):
    content = TruncatedField()

    class Meta(PostSerializer.Meta):
        exclude = None
        fields = ('id', 'title', 'date_submitted', 'last_reply', 'user', 'replies', 'content')


class PostImportSerializer(PostSerializer):
    id = serializers.CharField(source='payload_id')

    class Meta(PostSerializer.Meta):
        read_only_fields = ()


class PostBlockchainSerializer(PostSerializer):
    class Meta(PostSerializer.Meta):
        exclude = None
        fields = ('id', 'title', 'date_submitted', 'user_id', 'content', 'reply_to', 'signature')
        extra_kwargs = {}


class ReplySerializer(PostSerializer):
    class Meta(PostSerializer.Meta):
        exclude = None
        fields = ('id', 'date_submitted', 'block_time',
                  'user', 'content', 'signature', 'block_height')
