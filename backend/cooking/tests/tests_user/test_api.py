from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APITestCase


User = get_user_model()


class UserCreateDjoserSerializerTesCase(APITestCase):
    """return user info for djoser url='auth/users/me'"""

    def setUp(self):
        self.user1 = User.objects.create(username="jane", email="zoo@mail.com",password="12345")
        self.user2 = User.objects.create(username="jan", email="wood@mail.com",password="12345")

    def test_get_user(self):
        """ via djoser built-in view: get user"""
        self.client.force_authenticate(user=self.user1)
        url = '/auth/users/me'
        response = self.client.get(url)
        print("resp line 21",response)
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)

    # TODO
    # def test_delete_user(self):
    #     """via custom delete account; user auth-ed"""
    #     self.client.force_authenticate(user=self.user2)
    #     url = 'api/v1/users/me/'
    #     response = self.client.delete(url,data={'current_password':'12345'}) 
    #     print("resp is",response)
    #     self.assertEqual(response.status_code, 204) 404 status

    # def test_delete_user(self):
    #     """via custom delete account; user auth-ed"""
    #     self.client.force_authenticate(user=self.user2)
    #     url = reverse('delete-account')
    #     response = self.client.delete(url) 
    #     self.assertEqual(response.status_code, 204)

   
# self.user=self.client.post('/auth/users/',
# data={'username':'leo','email':'leo@mail.com','password':'12345aa','re_password':'12345aa'})
# def test_userprofile_unauthenticated(self):
# self.client.force_authenticate(user=None)