import json
import hashlib
import ecdsa
import codecs
import base58

from djongo import models
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from users.models import User
from categories.models import Category


def to_base58(s):
    return base58.b58encode_check(s).decode('ascii')


def from_base58(s):
    return base58.b58decode_check(s)


class PostManager(models.Manager):
    def create(self, **kwargs):

        print(kwargs)
        post = self.model(**kwargs)
        try:
            user = User.objects.get(nickname=kwargs['user_id'])
        except ObjectDoesNotExist:
            raise ValueError('User instance error.')

        print(user)

        postjson = json.loads(json.dumps(kwargs, sort_keys=True))
        print(postjson)
        postjson.pop('signature')
        postjson_hash = hashlib.sha256(json.dumps(postjson).encode('utf-8')).hexdigest()
        print(postjson_hash)

        uservk_string = user.public_key
        print(user.public_key)
        uservk_byte = from_base58(uservk_string)

        uservk = ecdsa.VerifyingKey.from_string(uservk_byte, curve=ecdsa.SECP256k1)
        assert uservk.verify(from_base58(post.signature), codecs.decode(postjson_hash, 'hex'))

        # category = Category.objects.get(name=post.category)
        # if not category:
        #     raise ValueError('Category "' + post.category + '" is not allowed.')
        # category.posts += 1
        #
        # reply_to = kwargs.get('reply_to')
        # master = None
        # if reply_to and len(reply_to) > 0:
        #     try:
        #         master = self.get(transaction_id=reply_to)
        #     except ObjectDoesNotExist:
        #         master = None
        # else:
        #     category.topics += 1
        #     if user:
        #         user.topics += 1
        #
        # if master:
        #     master.replies += 1
        #     if user:
        #         user.replies += 1
        #     master.last_reply = post.transaction_id
        #     post.category = master.category
        #     master.save()

        post.save()
        # category.save()
        if user:
            user.save()


        return self.get(id=post.id)


class Post(models.Model):
    id = models.ObjectIdField(db_column='_id', default=None)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=20000)

    user_id = models.CharField(max_length=100)

    # 使用 URI-liked 的形式，暂时仅允许第一级目录
    # TODO: 给 Post 的 category 字段添加 validator
    topic_id = models.CharField(max_length=255)
    signature = models.CharField(max_length=255)

    time_submitted = models.DateTimeField(default=timezone.now)
    # date_confirmed = models.DateTimeField(null=True, default=None)
    # is_confirmed = models.BooleanField(default=False)
    # block_height = models.IntegerField(default=0)

    # 对应另一个 Post 的 transaction_id
    # TODO: 暂时限制仅能回复 reply_to 字段为空的 post
    reply_to = models.CharField(max_length=128, null=True, db_index=True)
    replies = models.IntegerField(default=0)
    last_reply = models.CharField(max_length=128, null=True)

    # TODO: 用于编辑，对应原始 post 的 transaction_id
    # base_to = models.CharField(max_length=128, null=True)

    # TODO: 可能需要限制为 UV 而不是 PV
    # views = models.BigIntegerField(default=0)

    # TODO: 需要新的接口，对登录用户可用
    likes = models.BigIntegerField(default=0)

    objects = PostManager()

    class Meta:
        db_table = 'infnote_posts'
