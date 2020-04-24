import json
from datetime import timedelta
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from oauth2_provider.models import Application, AccessToken
from oauth2_provider.settings import oauth2_settings
from accounts.models import User


class UserTests(APITestCase):
    def setUp(self):
        oauth2_settings._SCOPES = ["read", "write", "scope1", "scope2", "resource1"]
        self.email = 'test@admin.co'
        self.password = 'admin'
        self.f_name = 'First'
        self.l_name = 'Last'
        self.user = User.objects.create_superuser(
            email=self.email,
            password=self.password,
            f_name=self.f_name,
            l_name=self.l_name
        )
        self.application = Application.objects.create(
            name="Test Application",
            redirect_uris="",
            user=self.user,
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.authorization_grant_type,
        )
        self.access_token = AccessToken.objects.create(
            user=self.user,
            scope="read write",
            expires=timezone.now() + timedelta(seconds=300),
            token="secret-access-token-key",
            application=self.application
        )

    @staticmethod
    def _create_authorization_header(token):
        return "Bearer {0}".format(token)

    def test_list_users(self):
        """
        Ensure we can list users created
        :return: void
        """
        auth = self._create_authorization_header(self.access_token.token)
        url = reverse('users-gc')
        response = self.client.get(url, HTTP_AUTHORIZATION=auth, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for key, value in response.data[0].items():
            if key == 'id':
                self.assertEqual(value, 1)
            if key == 'email':
                self.assertEqual(value, self.email)
            if key == 'f_name':
                self.assertEqual(value, self.f_name)
            if key == 'l_name':
                self.assertEqual(value, self.l_name)
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
        auth = self._create_authorization_header(self.access_token.token)
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
