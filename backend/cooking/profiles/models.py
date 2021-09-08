from django.db import models
from timestamp.models import TimeStamp
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from timestamp.broadcast_utils.idea_utils import upload_img
# from PIL import Image
from timestamp.broadcast_utils.validators import validate_size
from django.core.validators import FileExtensionValidator


ALLOWED_EXTENTIONS = ('JPG', 'JPEG', 'PNG')


User = get_user_model()


class Profile(TimeStamp):
    """ 
    unid instead for safer url;
    badge_bg (creat random bg-color by creating profile object)
    """
    # show_notifications = models.BooleanFieled(default=True)
    # show_subscription_notif =  models.BooleanFieled(default=True)  
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        # primary_key=True,
        related_name='profile'
    )
    unid = models.CharField(max_length=6, blank=True, db_index=True)
    image = models.ImageField(blank=True, null=True, upload_to=upload_img,
                              validators=[FileExtensionValidator(ALLOWED_EXTENTIONS), validate_size]) 
    bio = models.TextField(blank=True,default = "")                             
    website = models.URLField(max_length=100, default="", blank=True)
    badge_bg = models.CharField(max_length=30, default="", blank=True)
    following = models.ManyToManyField(User,related_name="followed_by",blank=True)
    remove_file = models.BooleanField(default=False)

   


    def __str__(self):
        return f"{self.user.username}"

    def get_absolute_url(self):
        return reverse('profiles:profile-info', kwargs={'profile_unid': self.unid})

    # def in_subscribers(self,user):
    #     """check if a given user id belongs to a list of (id's ) my subscribers"""
    #     return user.id in self.subscribed_to.values_list('id',flat=True)    
    
    # def in_followres(self):
    #     """check if a given user id belongs to a list of (id's ) my subscribers"""
    #     return self.id in self.followers.values_list('id',flat=True)    
    
    def get_name(self):
        if self.user.first_name and self.user.last_name:
            return '{} {}'.format(
                self.user.first_name.capitalize(),
                self.user.last_name.capitalize())
        else:
            return self.user.username

    # @property
    # def get_avatar_url(self, *args, **kwargs):
    #     """ return path to profile image """
    #     # if self.image:
    #     #     return f'/media/{self.image}'
    #     # else:
    #     return '/assets/img/avatar.png'

  
    
    # subscribed_to = models.ForeignKey(User,related_name='myfollowers',null=True,blank=True,on_delete=models.SET_NULL )
    # followers = models.ForeignKey(User,related_name='following',blank=True,null=True,on_delete=models.SET_NULL )
    