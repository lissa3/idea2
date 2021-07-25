from django.test import TestCase
from profiles.models import Profile
from api.serializers.account.profile_serializer import ProfileSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class ProfileSerializerTesCase(TestCase):
    """compare expected and received data after ser-on"""

    def setUp(self):
        self.user = User.objects.create(username="nick", email="zoo@mail.com")
        self.profile = Profile.objects.last()

    def test_profile_serializer(self):
        """ let op: not arr but dict; 
        id is set to string (see ser-er CharField(read_olnly) """
        serial_profile = ProfileSerializer(self.profile).data
        expected_data = {
            # "unid": self.profile.unid,
            # "user_id": self.user.id,
            "image": None,
            "website": "",
            "bio":"",
            "name":"nick"
            

        }
        self.assertEqual(serial_profile, expected_data)