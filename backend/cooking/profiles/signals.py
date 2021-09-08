from django.db.models.signals import post_save,pre_save,post_delete
from django.dispatch import receiver
from timestamp.broadcast_utils.base_utils import make_unid,create_color
from profiles.models import Profile
from django.contrib.auth import get_user_model
import logging


logger = logging.getLogger('user_issues')
User = get_user_model()

@receiver(post_delete,sender=Profile)
def auto_delete_user(sender,instance,**kwargs):
    try:
        instance.user
    except User.DoesNotExist:
        pass
    else:
        instance.user.delete()

#user created |==> create his profile
@receiver(post_save,sender=User)
def create_profile(sender,instance,created,*args,**kwargs):
    """create_or_update profile"""
    # print("inside post save signal; creating profile on user with is",instance.id,instance.email)
    try:
        if created and instance.email:
            Profile.objects.create(user=instance)
            logger.info(f'profile created for {instance.email}')
    except:
        logger.error('profile creation failed')
    finally:
        pass    

    


# before profile get saved in db |==> create unid,displayname,random bg color for avatar
@receiver(pre_save,sender= Profile)
def add_unid(sender,instance,**kwargs):
    # print("pre-save profile calling, creating uid")
    if not instance.unid:
        instance.unid = make_unid(instance)
        # print("profile instance gets unid",instance.unid)
    # if not instance.display_name:
    #     instance.display_name = make_display_name(instance)
    instance.badge_bg  = create_color()   