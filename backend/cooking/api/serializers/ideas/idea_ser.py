from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
# from django.core.validators import FileExtensionValidator

from rest_framework import serializers as ser
# help module for taggit
from taggit_serializer.serializers import (TagListSerializerField,
                                           TaggitSerializer)

from ideas.models import Idea
from timestamp.broadcast_utils.validators import validate_size
import logging
logger = logging.getLogger(__name__)

User = get_user_model()


class IdeaSerializer(TaggitSerializer, ser.ModelSerializer):    
    categ_name = ser.ReadOnlyField(source='categ.name')
    author_unid = ser.ReadOnlyField(source='author.unid',read_only=True)
    owner_idea = ser.CharField(source='author.username', default="", read_only=True)
    author = ser.PrimaryKeyRelatedField(queryset=User.objects.all(), default=ser.CurrentUserDefault())
    tags = TagListSerializerField(required=False) 
    # users_comments = ser.IntegerField(read_only=True) for postgresql
    users_comments = ser.SerializerMethodField()
    thumbnail = ser.ImageField(validators=[validate_size], required=False, allow_null=True)
    # ERROR: nexpected keyword argument 'allowed_extentions
    # thumbnail = ser.ImageField(validators=[validate_size], allowed_extentions=[
    #                            'jpeg', 'jpg', 'png'], required=False, allow_null=True)
    class Meta:
        model = Idea
        fields = ('id', 'title', 'author', 'lead_text', 'main_text', 'slug',
                  'owner_idea','author_unid','categ_name', 'categ', 'created_at', 'status', 'thumbnail', 
                  'avg_rate','an_likes', 'featured', 'tags','max_rating','users_comments','remove_file')

    def get_users_comments(self,obj):
        # temp solution ( till postgres overstap)
        return  obj.comments.count() 


    def save(self, *args, **kwargs):
        """ if idea has already thumbnail it will be replaced by a new img
        otherwise thumbnail attr gets a value(new img)
        # no img from front( img not attached or not changed(url to aws s3))
        validated data: OrderedDict([ ('thumbnail', None),('remove_file', False)])
        #TODO: 
        # user attached img: 
        validated data: ('thumbnail', <InMemoryUploadedFile: one.jpg (image/jpeg)>)
        
        """
        # print("inside serializer",dir(self))
        print("in ser-er")
        print(self.validated_data)  
        del_previous_file = self.validated_data.get('remove_file') 
        img = self.validated_data.get('thumbnail',None)   
        # print("img from validated data",img)
        try:
            print("in try block")
            if self.instance.pk and del_previous_file:                
            # if self.instance.pk and img is not None:                
                print("test: prev thumbnail was:",self.instance.thumbnail)     
                # если этого не будет,то из db thumbnail все равно выпилится, но в aws s3 будет продолжать болтаться
                self.instance.thumbnail.delete()
                print("deleted thumbnail from db? or from aws?")
            if self.instance.pk and img is None and del_previous_file: 
                self.instance.thumbnail.delete()
                print("deleted thumbnail from db? or from aws?")     
        except:
            print('in block except')        
        # print("") 
        super().save(*args,**kwargs)





    # def save(self, *args, **kwargs):
    #     """ if idea has already thumbnail it will be replaced by a new img
    #     otherwise thumbnail attr gets a value(new img)
    #     # no img from front 
    #     validated data: OrderedDict([ ('thumbnail', None),('remove_file', False)])
    #     if img === None|=> type(img) class NoneType
    #     # user attached img: 
    #     validated data: ('thumbnail', <InMemoryUploadedFile: one.jpg (image/jpeg)>)
        
    #     """
    #     # print("inside serializer",dir(self))
    #     print("in ser-er")
    #     print(self.validated_data)   
    #     img = self.validated_data.get('thumbnail',None)        
    #     try:
    #         print("in try block")
    #         if self.instance.pk:
    #             if img is not None:
    #                 print("img is not None")
    #                 # если этого не будет,то из db thumbnail все равно выпилится, но в aws s3 будет продолжать болтаться
    #                 self.instance.thumbnail.delete()
    #                 print("deleted thumbnail from db? or from aws?")
    #     except:
    #         print('in block except')        
    #     # print("") 
    #     super().save(*args,**kwargs)
        
    
       
        
        


    
     

    
"""
line 47 in save method of ser-er self.instance is: Balcon
line 52 inst dict is: {'_state': <django.db.models.base.ModelState object at 0x7fb616f7dc10>, 'id': 22, 'created_at': datetime.datetime(2021, 9, 3, 11, 37, 9, 25508, tzinfo=<UTC>), 'updated_at': datetime.datetime(2021, 9, 3, 12, 8, 17, 245790, tzinfo=<UTC>), 'author_id': 1, 'categ_id': 7, 'title': 'Balcon', 'slug': 'balcon', 'lead_text': 'Verzorgen', 'main_text': 'Met water en zo', 'view_count': 0, 'thumbnail': '', 'featured': False, 'is_public': True, 'status': 0, 'avg_rate': None, 'an_likes': 0, 'max_rating': None, 'remove_file': False, '_prefetched_objects_cache': {'tags': <QuerySet []>}}
before save {'_state': <django.db.models.base.ModelState object at 0x7fb616f7dc10>, 'id': 22, 'created_at': datetime.datetime(2021, 9, 3, 11, 37, 9, 25508, tzinfo=<UTC>), 'updated_at': datetime.datetime(2021, 9, 3, 12, 8, 17, 245790, tzinfo=<UTC>), 'author_id': 1, 'categ_id': 7, 'title': 'Balcon', 'slug': 'balcon', 'lead_text': 'Verzorgen', 'main_text': 'Met water en zo', 'view_count': 0, 'thumbnail': <ImageFieldFile: None>, 'featured': False, 'is_public': True, 'status': 0, 'avg_rate': None, 'an_likes': 0, 'max_rating': None, 'remove_file': False, '_prefetched_objects_cache': {'tags': <QuerySet []>}}




# if self.instance:
        #     logger.warning('instance already exists')
        #     print("line 53",self.instance.__dict__)
        #     try:
        #         if self.instance.thumbnail and self.instance.remove_file==True:
        #             print("line 51",self.instance.thumbnail)
        #             print("user wants to delete file; starting delete thumbnail ")
        #             self.instance.thumbnail.delete()
        #             logger.warning('user wants to delete file')
        #     except:
        #         print("nothing to delete in deleting inst img")    
        # else:
        #     print("instance does not exist yet") 
        #     logger.warning('New obj idea to be created')   
        # return super().save(*args, **kwargs) 
"""

    