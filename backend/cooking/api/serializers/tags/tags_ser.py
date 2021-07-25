from django.utils.translation import gettext_lazy as _
from rest_framework import serializers as ser

from taggit.models import Tag


class TagSerializer(ser.ModelSerializer):
    # tags = TagListSerializerField()
    id = ser.IntegerField(read_only=True)
    # id = ser.CharField(read_only=True)

    class Meta:
        model = Tag
        fields = ('id', 'slug', 'name',)