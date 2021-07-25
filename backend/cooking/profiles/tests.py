from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()

class UniqueDisplayNameTest(TestCase):
    def test_profile_get_name_property(self):
        user1 = User.objects.create(username="go",email="zoo@mail.com",password="abdhdhdhd")       
        user1_display_name = user1.profile.get_name        
        self.assertEqual(user1_display_name,"go")
        
    def test_unique_username(self):
        """check if name is unique"""
        user1 = User.objects.create(username="go",email="zoo@mail.com",password="abdhdhdhd")
        try:
            user2 = User.objects.create(username="go",email="zoo@yahoo.com",password="fgfggfgf")
        except:
            self.assertRaises(ValidationError) #,'UNIQUE constraint failed: users_user.username')


