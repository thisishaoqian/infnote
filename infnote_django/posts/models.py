from djongo import models
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from users.models import User


class PostManager(models.Manager):
    def create(self, **kwargs):
        post = self.model(**kwargs)
        try:
            user = User.objects.get(id=kwargs.get('user_id'))
        except ObjectDoesNotExist:
            raise ValueError('User is not exist.')

        post.save()

        if not post.reply_to:
            user.topics += 1
            user.save()
        else:
            try:
                topic = self.get(payload_id=post.reply_to)
            except ObjectDoesNotExist:
                return self.get(id=post.id)
            topic.replies += 1
            topic.last_reply = post.payload_id
            topic.save()
            topic_owner = User.objects.get(id=topic.user_id)
            topic_owner.replies += 1
            topic_owner.save()

        return self.get(id=post.id)


class Post(models.Model):
    # Local content
    id = models.ObjectIdField(db_column='_id', default=None)
    replies = models.IntegerField(default=0)
    last_reply = models.CharField(max_length=256, null=True)

    # User content
    title = models.CharField(max_length=100, null=True)
    content = models.CharField(max_length=20000)
    date_submitted = models.IntegerField(default=0)
    reply_to = models.CharField(max_length=256, null=True, db_index=True)
    user_id = models.CharField(max_length=100)

    signature = models.CharField(max_length=256)

    # Chain owner info
    payload_id = models.CharField(max_length=256, unique=True, db_index=True)
    block_time = models.IntegerField(default=0)
    block_height = models.IntegerField(default=0)

    objects = PostManager()

    class Meta:
        db_table = 'infnote_posts'
