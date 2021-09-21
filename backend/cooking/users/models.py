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
    # first_name = models.CharField(_('first_name'),max_length=120,default='',blank=True)
    # last_name = models.CharField(_('last_name'),max_length=120,default='',blank=True)
    email = models.EmailField(_('Email address'), unique=True, max_length=255)
    date_joined = models.DateTimeField(default=timezone.now)
    is_banned = models.BooleanField(default=False)
    blackListEmail = models.BooleanField(default=False)
    # uuid = models.UUIDField(db_index=True, unique=True, default=uuid.uuid4)
        
    USERNAME_FIELD = 'email'

    # REQUIRED_FIELDS: to create superuser: list containing other fields than UUSERNAME_FIELD
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def get_ava_letter(self):
        return self.username[0]    

    def __str__(self):
        return self.username
    def get_name(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'   
        else:
            return self.username     

