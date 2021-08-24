from django.contrib.auth import get_user_model
from django.db.models import Count

from rest_framework import serializers as ser
from profiles.models import Profile
from api.serializers.account.user_serializer import UserSerializer
from timestamp.broadcast_utils.validators import validate_size

User = get_user_model()




class ProfileSerializer(ser.ModelSerializer):
    """ serve crud operations on profile(via form) """
    user = UserSerializer(many=False,read_only=True)
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
            raise ser.ValidationError("Profile  does not exist")
        
              
        
    def get_count_following(self,obj):
        return obj.following.count() 

    def get_followers(self,obj): 
        """ qs of profiles(check)?"""  
        # user = self.context.get("request").user           
        qs = obj.user.followed_by.all() 
        if qs.count()>0:
            data = [{'unid': obj.unid, 'user_id': obj.id,'username': obj.user.username,'id':obj.user.id} for obj in qs] 
        else:
            data = []          
        return data  
    def get_count_followers(self,obj):
        """qs of profiles"""
        # user = self.context.get("request").user 
        count = obj.user.followed_by.count()       
        # data = [{'unid': obj.unid, 'user_id': obj.user_id,'username': obj.user.username} for obj in qs]       
        return count              

# class ProfilePublicSerializer(ser.ModelSerializer):
#     # user will give reversed data about user = profile followers
#     user = UserSerializer(many=False)
#     name = ser.ReadOnlyField(source='get_name')   
#     website = ser.URLField(required=False)    
#     image = ser.ImageField(validators=[validate_size], required=False, allow_null=True)
#     followers =  ser.SerializerMethodField()    
#     count_followers = ser.SerializerMethodField()

#     following = ser.SerializerMethodField()    
#     count_following = ser.IntegerField(read_only=True) # via annotated qs in view
    
    
#     class Meta:
#         model = Profile
#         fields = ('bio','website', 'image','name','unid','following','user','followers','count_following','count_followers')

#     def get_followers(self,obj): 
#         """"""            
#         qs = obj.user.followed_by.all()       
#         data = [{'unid': obj.unid, 'user_id': obj.user_id,'username': obj.user.username} for obj in qs]       
#         return data    

#     def get_following(self,obj): 
#         """"""                 
#         qs = obj.following.all()        
#         data = [{'unid': obj.profile.unid, 'username': obj.username,'id':obj.id} for obj in qs]
#         return data 

#     def get_count_followers(self,obj):
#         # return obj.user.followed_by.count()      
#         return obj.user.followed_by.count() 

           
           
         

     

   

        