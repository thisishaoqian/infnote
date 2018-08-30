import string
import random
import hashlib
import base58

from datetime import datetime, timedelta

from djongo import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password


class UserManager(models.DjongoManager):
    def create(self, email, nickname, public_key, signature, **kwargs):

        if not email or not nickname or not public_key or not signature:
            raise ValueError('email, nickname, public_key, signature are all required.')

        ripemd160 = hashlib.new('ripemd160')
        ripemd160.update(hashlib.sha256(public_key.encode('ascii')).digest())
        user_id = base58.b58encode_check(ripemd160.digest()).decode('ascii')

        user = self.model(user_id=user_id, email=email, nickname=nickname, public_key=public_key,
                          signature=signature, **kwargs)
        user.save()

        return self.get(email=email)

    def get_by_natural_key(self, username):
        return self.get(email=username)


class User(models.Model):
    GENDER_UNKNOWN = 0
    GENDER_MALE = 1
    GENDER_FEMALE = 2
    GENDER_CHOICES = (
        (GENDER_UNKNOWN, 'unknown'),
        (GENDER_MALE, 'male'),
        (GENDER_FEMALE, 'female'),
    )

    #id = models.ObjectIdField(db_column='_id', default=None)
    user_id = models.CharField(max_length=255, unique=True, primary_key=True)
    nickname = models.CharField(max_length=100, unique=True)
    public_key = models.CharField(max_length=255, unique=True)
    signature = models.CharField(max_length=255, unique=True)
    email = models.CharField(max_length=100, unique=True)

    date_created = models.DateTimeField(default=timezone.now)
    date_last_login = models.DateTimeField(default=timezone.now)

    # Personal information
    avatar = models.CharField(max_length=255, blank=True)
    gender = models.IntegerField(choices=GENDER_CHOICES, default=GENDER_UNKNOWN)
    date_birthday = models.DateTimeField(default=timezone.now)
    location = models.CharField(max_length=100, blank=True)
    bio = models.CharField(max_length=255, blank=True)

    # Social information
    website = models.CharField(max_length=255, blank=True)
    qq = models.CharField(max_length=50, blank=True)
    wechat = models.CharField(max_length=50, blank=True)
    weibo = models.CharField(max_length=50, blank=True)
    facebook = models.CharField(max_length=50, blank=True)
    twitter = models.CharField(max_length=50, blank=True)

    # Post relevant information
    topics = models.IntegerField(default=0)
    replies = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname']

    class Meta:
        db_table = 'infnote_users'

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.email


class CodeManager(models.Manager):
    def create(self, email):
        other_codes = self.filter(email=email, is_valid=True)
        for code in other_codes:
            code.is_valid = False
            code.save()

        code = ''.join(random.choices(string.digits, k=6))
        vcode = self.model(email=email, code=code, expires=datetime.utcnow() + timedelta(minutes=30))
        vcode.save()

        return vcode


class VerificationCode(models.Model):
    _id = models.ObjectIdField()
    email = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    expires = models.DateTimeField()
    is_valid = models.BooleanField(default=True)

    objects = CodeManager()

    class Meta:
        db_table = 'infnote_vcode'

    @classmethod
    def verify(cls, email, code):
        if not email or not code:
            return False

        vcodes = cls.objects.filter(email=email, code=code, expires__gt=datetime.utcnow(), is_valid=True)
        if len(vcodes) <= 0:
            return False

        for vcode in vcodes:
            vcode.is_valid = False
            vcode.save()

        return True
