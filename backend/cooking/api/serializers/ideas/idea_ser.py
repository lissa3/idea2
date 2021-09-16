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
logger = logging.getLogger('upload')

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

    # def create(self, validated_data):
    #     try:
    #         print("line 45 val data",validated_data)
    #         logger.warning(f'ser-er error create success')  
    #         # return super().create(**validated_data)
    #     except Exception as e:
    #         print("line 48 val data",e)
    #         logger.error(f'ser-er error create {e}')  
    #     else:
    #         return super().create(validated_data)

    

    def save(self, *args, **kwargs):
        """ if idea has already thumbnail it will be replaced by a new img
        otherwise thumbnail attr gets a value(new img)
        # no img from front( img not attached or not changed(url to aws s3))
        validated data: OrderedDict([ ('thumbnail', None),('remove_file', False)])
        #TODO: 
        # user attached img: 
        validated data: ('thumbnail', <InMemoryUploadedFile: one.jpg (image/jpeg)>)        
        """       
        del_previous_file = self.validated_data.get('remove_file') 
        img = self.validated_data.get('thumbnail',None)   
        print("img from validated data",img)
        # empty str in req.data|=>thumbnail == None
        # aws s3 url|=> thumbnail = None
        try:
            if self.instance.pk and img is None and del_previous_file: 
                """
                case: user removes prev image and sends empty str as thumbnail back;
                img should be deleted on aws s3
                """
                self.instance.thumbnail.delete()                
                logger.warning(f'user {self.instance.author} deleted img ')
            elif self.instance.pk and del_previous_file:
                """
                prevent formation of  orphan images on aws s3;
                without this block: new img will be linked with current idea but the old one with persist on aws3;
                cases: 
                1. prev file existed and replaces the old one
                2.prev file doesn't exist and a new file comes 
                """               
                self.instance.thumbnail.delete()  
                logger.warning(f'user {self.instance.author} deleted img from aws (and replaced it with a new one)')          
        except Exception as e:
                # ignore exception obj is just created and has no pk yet 
                logger.warning(f'General exception in idea ser-er {e}')
                    
        finally:
            pass         
        super().save(*args,**kwargs)  


    
     

    
"""
line 47 in save method of ser-er self.instance is: Balcon
line 52 inst dict is: {'_state': <django.db.models.base.ModelState object at 0x7fb616f7dc10>, 'id': 22, 'created_at': datetime.datetime(2021, 9, 3, 11, 37, 9, 25508, tzinfo=<UTC>), 'updated_at': datetime.datetime(2021, 9, 3, 12, 8, 17, 245790, tzinfo=<UTC>), 'author_id': 1, 'categ_id': 7, 'title': 'Balcon', 'slug': 'balcon', 'lead_text': 'Verzorgen', 'main_text': 'Met water en zo', 'view_count': 0, 'thumbnail': '', 'featured': False, 'is_public': True, 'status': 0, 'avg_rate': None, 'an_likes': 0, 'max_rating': None, 'remove_file': False, '_prefetched_objects_cache': {'tags': <QuerySet []>}}
before save {'_state': <django.db.models.base.ModelState object at 0x7fb616f7dc10>, 'id': 22, 'created_at': datetime.datetime(2021, 9, 3, 11, 37, 9, 25508, tzinfo=<UTC>), 'updated_at': datetime.datetime(2021, 9, 3, 12, 8, 17, 245790, tzinfo=<UTC>), 'author_id': 1, 'categ_id': 7, 'title': 'Balcon', 'slug': 'balcon', 'lead_text': 'Verzorgen', 'main_text': 'Met water en zo', 'view_count': 0, 'thumbnail': <ImageFieldFile: None>, 'featured': False, 'is_public': True, 'status': 0, 'avg_rate': None, 'an_likes': 0, 'max_rating': None, 'remove_file': False, '_prefetched_objects_cache': {'tags': <QuerySet []>}}
"""

    