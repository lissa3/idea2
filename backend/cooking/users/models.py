from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .managers import CustomUserManager


class User(AbstractUser):
    """ signup: username and email
    login: email
    """
    username = models.CharField(_("Username"), unique=True, max_length=120)
    email = models.EmailField(_('Email address'), unique=True, max_length=255)
    date_joined = models.DateTimeField(default=timezone.now)
    is_banned = models.BooleanField(default=False)
    blackListEmail = models.BooleanField(default=False)
    # TODO: check flow signup active via admin vs front (djoser)
    # subscribers = models.ManyToManyField(
    #             'self',related_name = 'subscriptions',symmetrical=False,blank=True)
    # show_notifications = models.BooleanFieled(default=True)
    # show_subscription_notif =  models.BooleanFieled(default=True)

    # def in_subscribers(self,user):
    #     return user.id in self.subscribers.values_list('id',flat=True)

    USERNAME_FIELD = 'email'

    # REQUIRED_FIELDS: to create superuser: list containing other fields than UUSERNAME_FIELD
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def get_ava_letter(self):
        return self.username[0]    

    def __str__(self):
        return self.username

