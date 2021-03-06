from django.db import models
# from postchiapp import utils
# from model_utils import Choises
#  TODO: install package model_utils
from tg_handler import models as tg
from django.contrib.auth.models import AbstractUser, BaseUserManager
# Create your models here.


class AccountManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have a valid email address.')
        if not kwargs.get('username'):
            raise ValueError('Users must have a valid username.')

        account = self.model(
            email=self.normalize_email(email), username=kwargs.get('username')
        )
        account.set_password(password)
        account.save()

        return account

    def create_superuser(self, email, password, **kwargs):
        account = self.create_user(email, password, **kwargs)
        account.is_admin = True
        account.save()
        return account


class Account(AbstractUser):
    # CHECK THIS OUT:
    # https://stackoverflow.com/questions/10052220/advantages-to-using-urlfield-over-textfield
    # https://stackoverflow.com/questions/34743482/how-to-separate-users-models-by-admins-and-customers-on-django
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=40, unique=True)
    first_name = models.CharField(max_length=40, blank=True)
    last_name = models.CharField(max_length=40, blank=True)

    is_admin = models.BooleanField(default=False)

    bio = models.CharField(max_length=200, blank=True)
    website_url = models.URLField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __unicode__(self):
        return self.email

    def get_full_name(self):
        return ' '.join([self.first_name, self.last_name])

    def get_short_name(self):
        return self.first_name


# class Platform(models.Model):
#     identifier = models.CharField()

# class Post(models.Model):
#     text = models.TextField()
#     media = models.FileField()  # Assumption: We support only one media per each post


# class TelegramChatID(models.Model):
#     TYPES = Choises(
#         0, 'channel', _('channel'),
#         1, 'user', _('user'),
#         2, 'bot', _('bot'),
#     )
#
#     chat_id = models.CharField()
#     type = models.IntegerField(choices=TYPES, default=TYPES.channel)


class TwitterPlatform(models.Model):
    username = models.CharField(max_length=100, blank=True)  # For showing in profile?
    access_token = models.CharField(max_length=100, blank=True)


class InstagramPlatform(models.Model):
    username = models.CharField(max_length=100, blank=True)  # Instagram username
    password = models.CharField(max_length=100, blank=True)  # Instagram password ( saved encrypted ;) )


class Channel(models.Model):
    name = models.CharField(max_length=50, blank=False)  # i.e. کانون هواداران اینترمیلان
    channel_username = models.CharField(max_length=20, unique=True)  # i.e. inter_iran # Used to access channel

    photo = models.ImageField(null=True)
    about = models.TextField(null=True)

    # posts = models.ForeignKey(post.Post, on_delete=models.SET_NULL, null=True)

    # favorite_hashtags = ?
    #  TODO: Supporting signs and default hashtags for posts!

    tg = models.OneToOneField(tg.TelegramPlatform, on_delete=models.SET_NULL, null=True)

    tw = models.OneToOneField(TwitterPlatform, on_delete=models.SET_NULL, null=True)

    insta = models.OneToOneField(InstagramPlatform, on_delete=models.SET_NULL, null=True)

    admins = models.ManyToManyField(Account, related_name='admins', blank=True)
    owner = models.ForeignKey(Account, on_delete=models.CASCADE, editable=False, null=False, related_name='owner')

    def __unicode__(self):
        return self.channel_username
