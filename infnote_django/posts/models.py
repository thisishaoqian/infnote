import string
from random import choices

from djongo import models
from django.utils import timezone

from users.models import User


class PostManager(models.Manager):
    def create(self, user: User, **kwargs):
        if not isinstance(user, User):
            raise ValueError('User instance error.')
        transaction_id = ''.join(choices(string.ascii_letters + string.digits, k=20))
        post = self.model(
            public_key=user.public_key,
            transaction_id=transaction_id,
            **kwargs
        )

        reply_to = kwargs.get('reply_to')
        if reply_to and len(reply_to) > 0:
            master = self.get(transaction_id=reply_to)
            master.replies += 1
            post.save()
            master.save()
        else:
            post.save()

        return self.get(transaction_id=transaction_id)


class Post(models.Model):
    id = models.ObjectIdField(db_column='_id', default=None)
    title = models.CharField(max_length=100, blank=True)
    content = models.CharField(max_length=20000)

    # 使用 URI-liked 的形式，暂时仅允许第一级目录
    # TODO: 给 Post 的 category 字段添加 validator
    category = models.CharField(max_length=255)

    date_submitted = models.DateTimeField(default=timezone.now)
    date_confirmed = models.DateTimeField(null=True, blank=True, default=None)
    transaction_id = models.CharField(max_length=100, unique=True, null=True)
    is_confirmed = models.BooleanField(default=False)
    block_height = models.IntegerField(default=0)

    # 对应另一个 Post 的 transaction_id
    # TODO: 暂时限制仅能回复 reply_to 字段为空的 post
    reply_to = models.CharField(max_length=100, null=True, blank=True, db_index=True)

    # 发送者的 public key address
    public_key = models.CharField(max_length=100)

    # TODO: 可能需要限制为 UV 而不是 PV
    views = models.BigIntegerField(default=0)

    # TODO: 需要新的接口，对登录用户可用
    likes = models.BigIntegerField(default=0)

    replies = models.IntegerField(default=0)

    objects = PostManager()

    class Meta:
        db_table = 'infnote_posts'
