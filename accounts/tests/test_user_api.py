import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.tests.helper.oauth_helper import OauthHelper


class UserTests(APITestCase):
    def setUp(self):
        self.oauth = OauthHelper()
        self._application = OauthHelper.get_application(self.oauth)
        self._access_token = OauthHelper.get_access_token(self.oauth)
        self._admin_credentials = OauthHelper.get_admin_credentials(self.oauth)

    @staticmethod
    def _create_authorization_header(token):
        return "Bearer {0}".format(token)

    def test_list_users(self):
        """
        Ensure we can list users created
        :return: void
        """
        auth = self._create_authorization_header(self._access_token.token)
        url = reverse('users-gc')
        response = self.client.get(url, HTTP_AUTHORIZATION=auth, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for key, value in response.data[0].items():
            if key == 'id':
                self.assertEqual(value, 1)
            if key == 'email':
                self.assertEqual(value, self._admin_credentials["email"])
            if key == 'f_name':
                self.assertEqual(value, self._admin_credentials["f_name"])
            if key == 'l_name':
                self.assertEqual(value, self._admin_credentials["l_name"])
            if key == 'is_admin':
                self.assertEqual(value, True)
            if key == 'is_staff':
                self.assertEqual(value, True)
            if key == 'is_active':
                self.assertEqual(value, True)

    def test_user_create(self):
        """
        Ensure we can create users using restAPI
        :return: void
        """
        auth = self._create_authorization_header(self._access_token.token)
        url = reverse('users-gc')
        data = json.dumps({
            'email': 'test@user.co',
            'password': 'veryC0mpl3x$%',
            'f_name': 'Test',
            'l_name': 'User'
        })
        content_type = 'application/json'
        response = self.client.post(url, data=data, content_type=content_type, HTTP_AUTHORIZATION=auth)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        for key, value in response.data.items():
            if key == 'id':
                self.assertEqual(value, 2)
            if key == 'email':
                self.assertEqual(value, 'test@user.co')
            if key == 'f_name':
                self.assertEqual(value, 'Test')
            if key == 'l_name':
                self.assertEqual(value, 'User')
            if key == 'is_admin':
                self.assertEqual(value, False)
            if key == 'is_staff':
                self.assertEqual(value, False)
            if key == 'is_active':
                self.assertEqual(value, True)
