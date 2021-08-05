from django.contrib.auth import get_user_model
from django.db.models import Count

from rest_framework import serializers as ser
from profiles.models import Profile
from api.serializers.account.user_serializer import UserSerializer
from timestamp.broadcast_utils.validators import validate_size

User = get_user_model()




class ProfileSerializer(ser.ModelSerializer):
    # private: serves crud operations on profile(via form)
    name = ser.ReadOnlyField(source='get_name')     
    website = ser.URLField(required=False)    
    image = ser.ImageField(validators=[validate_size], required=False, allow_null=True)
    # let op: without allow_null = can't remove file from form and send to backend
    # to learn: image = serializers.ImageField(max_length=None, use_url=True)
    followers =  ser.SerializerMethodField()    
    count_followers = ser.SerializerMethodField()

    following = ser.SerializerMethodField()    
    count_following = ser.SerializerMethodField()  # via annotated qs in view

    class Meta:
        model = Profile
        fields = ('bio','website','unid','image','name','following','user','followers','count_following','count_followers')
        # fields = ('bio','website', 'image','name','count_following')
       
    def get_following(self, obj):
        """qs of users """
        print("obj class",obj.__class__)
        try:
            qs = obj.following.all()    
            if qs.count()>0:
                data = [{'unid': user.profile.unid, 'user_id': user.id,'username': user.username,'id':user.id} for user in qs] 
            else:
                data = []    
            return data             
        except Profile.DoesNotExist:
            raise ser.ValidationError("Profile of this user does not exist")
        
    def get_count_followers(self,obj):
        """qs of profiles"""
        user = self.context.get("request").user            
        return user.followed_by.count() 

    def get_count_following(self,obj):
        return obj.following.count() 

    def get_followers(self,obj): 
        """ qs of profiles(check)?"""  
        user = self.context.get("request").user           
        qs = user.followed_by.all() 
        if qs.count()>0:
            data = [{'unid': profile.unid, 'user_id': profile.id,'username': profile.user.username,'id':user.id} for profile in qs] 
        else:
            data = []          
        return data         

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
        fields = ('bio','website', 'image','name','unid','following','user','followers','count_following','count_followers')

    def get_followers(self,obj): 
        """"""            
        qs = obj.user.followed_by.all()       
        data = [{'unid': obj.unid, 'user_id': obj.user_id,'username': obj.user.username} for obj in qs]       
        return data    

    def get_following(self,obj): 
        """"""                 
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
           
         

     

   

        