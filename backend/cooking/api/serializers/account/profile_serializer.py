from django.contrib.auth import get_user_model
from rest_framework import serializers as ser
from profiles.models import Profile
from api.serializers.account.user_serializer import UserSerializer
from timestamp.broadcast_utils.validators import validate_size

User = get_user_model()

class ProfileSerializer(ser.ModelSerializer):
    # TODO: do I need it? 
    user = UserSerializer(many=False)
    name = ser.ReadOnlyField(source='get_name')   
    website = ser.URLField(required=False)    
    image = ser.ImageField(validators=[validate_size], required=False, allow_null=True)
    followed =  ser.SerializerMethodField()
    # let op: without allow_null = can't remove file from form and send to backend

    # following = ser.SlugRelatedField(slug_field="username", read_only=True, many=True)
    following = ser.SerializerMethodField()
    # count_following = ser.IntegerField(read_only=True)    
    
    
    class Meta:
        model = Profile
        fields = ('bio','website', 'image','name','following','user','followed')

    def get_followed(self,obj):        
        qs = obj.user.followed_by.all()
        print("line 29",qs)
        data = [{'unid': obj.unid, 'user_id': obj.user_id, 'username': obj.user.username} for obj in qs]
        return data  

    def get_following(self,obj):        
        qs = obj.following.all()
        print("line 34",qs)
        data = [{'unid': obj.profile.unid, 'username': obj.username} for obj in qs]
        return data  

    # def get_followed(self, obj):
    #     context = self.context
    #     request = context.get("request")
    #     qs = request.user.followed_by.all()
    #     data = [{'id': obj.pk, 'user_id': obj.user_id,'username':obj.user.username} for obj in qs]
    #     # data = [{'id': obj.pk, 'user_id': obj.user_id, 'name': obj.req_field} for obj in qs]
    #     return data    
       
"""
context
{'request': <rest_framework.request.Request: GET '/api/v1/profile-info/1/'>,
'format': None, 
'view': <api.views.ProfileRetrView object at 0x7ff69ca393d0>}
"""    
    


        