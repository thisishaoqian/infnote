from djongo import models
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from users.models import User


class PostManager(models.Manager):
    def create(self, **kwargs):
        post = self.model(**kwargs)
        try:
            user = User.objects.get(nickname=kwargs['user_id'])
        except ObjectDoesNotExist:
            raise ValueError('User instance error.')

        post.save()
        if user:
            user.save()

        return self.get(id=post.id)


class Post(models.Model):
    # Local content
    id = models.ObjectIdField(db_column='_id', default=None)
    replies = models.IntegerField(default=0)
    last_reply = models.CharField(max_length=256, null=True)

    # User content
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=20000)
    signature = models.CharField(max_length=256)

    # Server content
    user_id = models.CharField(max_length=100)
    date_submitted = models.DateTimeField(default=timezone.now)
    reply_to = models.CharField(max_length=256, null=True, db_index=True)

    # Chain owner info
    payload_id = models.CharField(max_length=256)
    date_confirmed = models.DateTimeField(null=True, default=None)
    is_confirmed = models.BooleanField(default=False)
    block_height = models.IntegerField(default=0)

    objects = PostManager()

    class Meta:
        db_table = 'infnote_posts'
