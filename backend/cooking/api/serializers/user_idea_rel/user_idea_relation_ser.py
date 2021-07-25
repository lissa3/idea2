from django.contrib.auth import get_user_model
from rest_framework import serializers as ser
from ideas.models import UserIdeaRelation

User = get_user_model()


class UserIdeaRelSerializer(ser.ModelSerializer):
    """ custom attr to display add/remove likes """
    # rating = ser.IntegerField(required=False)
    # an_likes = ser.IntegerField(read_only=True)

    class Meta:
        model = UserIdeaRelation
        fields = (
            'like', 'rating'
        )