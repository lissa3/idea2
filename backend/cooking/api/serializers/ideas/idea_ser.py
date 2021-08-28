from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
# from django.core.validators import FileExtensionValidator

from rest_framework import serializers as ser
# help module for taggit
from taggit_serializer.serializers import (TagListSerializerField,
                                           TaggitSerializer)

from ideas.models import Idea
from timestamp.broadcast_utils.validators import validate_size


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
                  'avg_rate','an_likes', 'featured', 'tags','max_rating','users_comments')

    def get_users_comments(self,obj):
        # temp solution ( till postgres overstap)
        return  obj.comments.count() 


    def save(self, *args, **kwargs):
        """ if idea has already thumbnail it will be replaced by a new img
        otherwise thumbnail attr gets a value(new img)
        """
        print("line 41 in save methof of ser-er self.instance is:",self.instance)
        if self.instance.thumbnail:
            print("line 42 found self.instance.thumbnail")
            print("starting delete thumbnail")
            self.instance.thumbnail.delete()
        else:
            print("thumbnail attr not found")    
        return super().save(*args, **kwargs)    

    
"""
self line 40 Boter forever
None
update ser-er method, obj is {'title': 'Boter forever', 'author': <User: tata>, 'lead_text': 'fast and tasty', 'main_text': 'Take not long', 'categ': <Category: Koekjes>, 'thumbnail': None, 'featured': False}

"""        

    # def update(self, instance, validated_data):
    #     instance.email = validated_data.get('email', instance.email)
    #     instance.content = validated_data.get('content', instance.content)
    #     instance.created = validated_data.get('created', instance.created)
    #     return instance
        
    # for testing orm ( without comments)     
    # class Meta:
    #     model = Idea
    #     fields = ('id', 'title', 'author', 'lead_text', 'main_text', 'slug',
    #               'owner_idea','author_unid','categ_name', 'categ', 'created_at', 'status', 'thumbnail', 'an_likes', 'avg_rate', 'featured', 'tags','max_rating')


    