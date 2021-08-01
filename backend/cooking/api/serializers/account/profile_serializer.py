from django.contrib.auth import get_user_model
from django.db.models import Count

from rest_framework import serializers as ser
from profiles.models import Profile
from api.serializers.account.user_serializer import UserSerializer
from timestamp.broadcast_utils.validators import validate_size

User = get_user_model()




class ProfileSerializer(ser.ModelSerializer):
    # no following followers info but option to crud operations
    name = ser.ReadOnlyField(source='get_name')     
    website = ser.URLField(required=False)    
    image = ser.ImageField(validators=[validate_size], required=False, allow_null=True)
    # let op: without allow_null = can't remove file from form and send to backend
    # to learn: image = serializers.ImageField(max_length=None, use_url=True)

    class Meta:
        model = Profile
        fields = ('bio','website', 'image','name')
        # fields = ('user_id', 'unid', 'website', 'image') 

class ProfilePublicSerializer(ser.ModelSerializer):
    # user will give reversed data about user = profile followers
    user = UserSerializer(many=False)
    name = ser.ReadOnlyField(source='get_name')   
    website = ser.URLField(required=False)    
    image = ser.ImageField(validators=[validate_size], required=False, allow_null=True)
    followers =  ser.SerializerMethodField()    
    count_followers = ser.SerializerMethodField()

    following = ser.SerializerMethodField()    
    count_following = ser.IntegerField(read_only=True) # via annotated qs in view
    
    
    class Meta:
        model = Profile
        fields = ('bio','website', 'image','name','following','user','followers','count_following','count_followers')

    def get_followers(self,obj): 
        """current user(profile) should be excluded from list"""            
        qs = obj.user.followed_by.all()       
        data = [{'unid': obj.unid, 'user_id': obj.user_id,'username': obj.user.username} for obj in qs]       
        return data    

    def get_following(self,obj): 
        """current user(profile) should be excluded from list"""                 
        qs = obj.following.all()        
        data = [{'unid': obj.profile.unid, 'username': obj.username,'id':obj.id} for obj in qs]
        return data 

    def get_count_followers(self,obj):
        # return obj.user.followed_by.count()      
        return obj.user.followed_by.count() 

    # def update(self, instance, validated_data):
    #     instance.title = validated_data.get('title', instance.title)
    #     instance.description = validated_data.get('description', instance.description)
    #     instance.body = validated_data.get('body', instance.body)
    #     instance.author_id = validated_data.get('author_id', instance.author_id)

    #     instance.save()
    #     return instance        
           
         

     

   

        