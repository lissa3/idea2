from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from rest_framework import serializers as ser
# help module for taggit
from taggit_serializer.serializers import (TagListSerializerField,
                                           TaggitSerializer)

from ideas.models import Idea


User = get_user_model()


class IdeaTestSerializer(TaggitSerializer, ser.ModelSerializer):

    categ_name = ser.ReadOnlyField(source='categ.name')

    """ ONLY FOR TESTING:excl created_at: for testing """
    # print("inside IdeaTestSer-er")
    owner_idea = ser.CharField(source='author.username', default="", read_only=True)
    an_likes = ser.IntegerField(read_only=True)
    avg_rate = ser.DecimalField(read_only=True, max_digits=5, decimal_places=2, default='0.00')
    author = ser.PrimaryKeyRelatedField(queryset=User.objects.all(),
                                        default=ser.CurrentUserDefault())

    categ_name = ser.ReadOnlyField(source='categ.name')

    tags = TagListSerializerField(required=False)
    # users_comments = ser.IntegerField(read_only=True)

    class Meta:
        model = Idea

        fields = ('id', 'title', 'author', 'lead_text', 'main_text', 'slug',
                  'owner_idea', 'categ_name', 'categ', 'status', 'an_likes', 'avg_rate', 'featured', 'tags', )
        print("ser-er class Meta?")

        fields = (
            'id', 'slug', 'title', 'author', 'lead_text', 'main_text', 'owner_idea', 'categ_name', 'categ', 'status', 'an_likes', 'avg_rate', 'featured', 'tags', 

        )

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields["tags"].error_messages["max_length"] = "max length! or too much"