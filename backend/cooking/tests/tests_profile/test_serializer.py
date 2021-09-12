from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.models import Count

from api.serializers.account.user_serializer import UserSerializer
from api.serializers.account.profile_serializer import ProfileSerializer #,ProfilePublicSerializer
from profiles.models import Profile

User = get_user_model()
"""
{ 'name': 'nick', 'unid': '93eKw', 'following': [], 'user': OrderedDict([('id', 1), ('username', 'nick'), ('unid', '93eKw')]), 'followers': [], 'count_following': 0, 'count_followers': 0}

"""

# class ProfilePublicSerializerTesCase(TestCase):
#     """compare expected and received data after ser-on"""

#     def setUp(self):
#         self.user = User.objects.create(username="nick", email="zoo@mail.com")
#         self.profiles = Profile.objects.annotate(count_following=Count('following')).select_related('user').prefetch_related('following')
#         self.profile = self.profiles.last()        

#     def test_profile_serializer(self):
#         """ let op: not arr but dict; 
#         id is set to string (see ser-er CharField(read_olnly) """
#         serial_profile = ProfilePublicSerializer(self.profile).data
#         expected_data = {
#             'user':{"id": self.user.id,"username": self.user.username,"unid": self.profile.unid},
#             'image': None,
#             'unid':self.profile.unid,
#             'website': '',
#             'bio':'',
#             'name':'nick',
#             'count_followers':0,
#             'count_following':0,
#             'followers':[],
#             'following':[]
            

#         }
#         # print("local",expected_data)
#         self.assertEqual(serial_profile, expected_data)


class ProfileSerializerTesCase(TestCase):
    """compare expected and received data after ser-on"""

    def setUp(self):
        self.user = User.objects.create(username="nick", email="zoo@mail.com")
        print("followers?",self.user.followed_by.all())
        self.profiles =  Profile.objects.all() 
        # print("profiles",self.profiles)        
        self.profile = self.profiles.last()        

    def test_profile_serializer(self):
        """ let op: not arr but dict; 
        id is set to string (see ser-er CharField(read_only) """
        serial_profile = ProfileSerializer(self.profile).data
        print("from view",serial_profile)
        expected_data = {            
            'image': None,
            'website': "",
            'bio':'',
            'unid':self.profile.unid,
            'name':'nick',
            'following':[],
            'followers':[],
            'count_following':0,
            'count_followers':0,
            'user':{"id": self.user.id,"username": self.user.username,"unid": self.profile.unid},
            'remove_file':False          
        
        }
        # print("local",expected_data)
        self.assertEqual(serial_profile, expected_data)
