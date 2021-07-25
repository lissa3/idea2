from django.db.models.signals import post_save,pre_save,post_delete
from django.dispatch import receiver
from timestamp.broadcast_utils.base_utils import make_unid,create_color
from profiles.models import Profile
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_delete,sender=Profile)
def auto_delete_user(sender,instance,**kwargs):
    instance.user.delete()

#user created |==> create his profile
@receiver(post_save,sender=User)
def create_profile(sender,instance,created,*args,**kwargs):
    """create_or_update profile"""
    if created and instance.email:
        Profile.objects.create(user=instance)
    # instance.profile.save()  # think if this line(errr in api/idea/tests) err:User has no profile 


# before profile get saved in db |==> create unid,displayname,random bg color for avatar
@receiver(pre_save,sender= Profile)
def add_unid(sender,instance,**kwargs):
    # print("pre-save profile calling, creating uid")
    if not instance.unid:
        instance.unid = make_unid(instance)
    # if not instance.display_name:
    #     instance.display_name = make_display_name(instance)
    instance.badge_bg  = create_color()   