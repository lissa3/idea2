from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.models import Count

from api.serializers.account.user_serializer import UserSerializer
from api.serializers.account.profile_serializer import ProfileSerializer,ProfilePublicSerializer
from profiles.models import Profile

User = get_user_model()


class ProfilePublicSerializerTesCase(TestCase):
    """compare expected and received data after ser-on"""

    def setUp(self):
        self.user = User.objects.create(username="nick", email="zoo@mail.com")
        print("followers?",self.user.followed_by.all())
        self.profiles =  Profile.objects.all().annotate(
                count_following=Count('following'),
                
                ) 
        # print("profiles",self.profiles)        
        self.profile = self.profiles.last()        

    def test_profile_serializer(self):
        """ let op: not arr but dict; 
        id is set to string (see ser-er CharField(read_olnly) """
        serial_profile = ProfilePublicSerializer(self.profile).data
        print("from view",serial_profile)
        expected_data = {
            'user':{"id": self.user.id,"username": self.user.username,"unid": self.profile.unid},
            'image': None,
            'website': "",
            'bio':'',
            'name':'nick',
            'count_followers':0,
            'count_following':0,
            'followed':[],
            'following':[]
            

        }
        # print("local",expected_data)
        self.assertEqual(serial_profile, expected_data)


class ProfileSerializerTesCase(TestCase):
    """compare expected and received data after ser-on"""

    def setUp(self):
        self.user = User.objects.create(username="nick", email="zoo@mail.com")
        print("followers?",self.user.followed_by.all())
        self.profiles =  Profile.objects.all().annotate(
                count_following=Count('following'),
                
                ) 
        # print("profiles",self.profiles)        
        self.profile = self.profiles.last()        

    def test_profile_serializer(self):
        """ let op: not arr but dict; 
        id is set to string (see ser-er CharField(read_olnly) """
        serial_profile = ProfileSerializer(self.profile).data
        print("from view",serial_profile)
        expected_data = {            
            'image': None,
            'website': "",
            'bio':'',
            'name':'nick',           
        
        }
        # print("local",expected_data)
        self.assertEqual(serial_profile, expected_data)

