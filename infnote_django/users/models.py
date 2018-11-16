from djongo import models
from django.contrib.auth.hashers import make_password, check_password


class UserManager(models.DjongoManager):
    def create(self, id, public_key, **kwargs):
        if not public_key or not id:
            raise ValueError('email, nickname, public_key, signature are all required.')

        user = self.model(id=id, public_key=public_key, **kwargs)
        user.save()

        return self.get(id=id)

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

    # User content
    id = models.CharField(max_length=100, unique=True, primary_key=True)
    nickname = models.CharField(max_length=100, unique=True)
    email = models.CharField(max_length=100, null=True)
    avatar = models.CharField(max_length=256, null=True)
    gender = models.IntegerField(choices=GENDER_CHOICES, default=GENDER_UNKNOWN)
    bio = models.CharField(max_length=256, null=True)

    # Key
    public_key = models.CharField(max_length=100, unique=True, db_index=True)
    signature = models.CharField(max_length=100, null=True)

    # Local info
    topics = models.IntegerField(default=0)
    replies = models.IntegerField(default=0)
    date_created = models.IntegerField(default=0)

    # Blockchain
    block_height = models.IntegerField(default=0)
    block_time = models.IntegerField(default=0)

    objects = UserManager()

    USERNAME_FIELD = 'id'
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
        return self.nickname + ' : ' + self.email
