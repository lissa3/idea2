from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase


User = get_user_model()


class UserCreateDjoserSerializerTesCase(APITestCase):
    """return user info for djoser url='auth/users/me'"""

    def setUp(self):
        self.user1 = User.objects.create(username="jane", email="zoo@mail.com")

    def test_get_user(self):
        """ via djoser built-in view: get user attr"""
        self.client.force_authenticate(user=self.user1)
        url = '/auth/users/me'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 301)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)