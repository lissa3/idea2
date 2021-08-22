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
    # an_likes = ser.IntegerField(read_only=True)
    # avg_rate = ser.DecimalField(read_only=True, max_digits=5, decimal_places=2, default='0.00')
    max_rating = ser.DecimalField(read_only=True, max_digits=5, decimal_places=2, default='0.00')
    author = ser.PrimaryKeyRelatedField(queryset=User.objects.all(), default=ser.CurrentUserDefault())
    tags = TagListSerializerField(required=False) 
    users_comments = ser.IntegerField(read_only=True)
    # users_comments = ser.SerializerMethodField()
    thumbnail = ser.ImageField(validators=[validate_size], required=False, allow_null=True)
    # ERROR: nexpected keyword argument 'allowed_extentions
    # thumbnail = ser.ImageField(validators=[validate_size], allowed_extentions=[
    #                            'jpeg', 'jpg', 'png'], required=False, allow_null=True)
    class Meta:
        model = Idea
        fields = ('id', 'title', 'author', 'lead_text', 'main_text', 'slug',
                  'owner_idea','author_unid','categ_name', 'categ', 'created_at', 'status', 'thumbnail', 
                  'rating','likes', 'featured', 'tags','max_rating','users_comments')

    # def get_users_comments(self,obj):
    #     # temp solution ( till postgres overstap)
    #     return  obj.comments.count()  
    # for testing orm ( without comments)     
    # class Meta:
    #     model = Idea
    #     fields = ('id', 'title', 'author', 'lead_text', 'main_text', 'slug',
    #               'owner_idea','author_unid','categ_name', 'categ', 'created_at', 'status', 'thumbnail', 'an_likes', 'avg_rate', 'featured', 'tags','max_rating')