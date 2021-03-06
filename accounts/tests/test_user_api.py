import json

from django.contrib.auth import authenticate
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User
from accounts.tests.helper.oauth_helper import OauthHelper


class UserTests(APITestCase):
    @staticmethod
    def __create_authorization_header(token):
        return "Bearer {0}".format(token)

    def setUp(self):
        self.__test_super_user = User.objects.create_superuser(
            f_name="Test",
            l_name="Super",
            email="super@user.co",
            password="VeryComplex#$123"
        )
        self.__test_user = User.objects.create_user(
            f_name="Test",
            l_name="User",
            email="test@user.co",
            password="VeryComplex#$123"
        )
        self.__oauth = OauthHelper(self.__test_super_user, ["read", "write"])
        self.__access_token = OauthHelper.get_access_token(self.__oauth)
        self.__auth = self.__create_authorization_header(self.__access_token.token)
        self.__admin_credentials = dict({
                "email": self.__test_super_user.email,
                "password": self.__test_super_user.password,
                "f_name": self.__test_super_user.f_name,
                "l_name": self.__test_super_user.l_name
            })
        self.__users_list_url = reverse("user-accounts:users-list")
        self.__user_detail_url = reverse("user-accounts:user-detail", kwargs={'pk': self.__test_user.pk})
        self.__user_update_pw_url = reverse("user-accounts:update-password")

    def test_list_users(self):
        """
        Ensure we can list users created
        :return: void
        """
        response = self.client.get(self.__users_list_url, HTTP_AUTHORIZATION=self.__auth, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for key, value in response.data[0].items():
            if key == 'id':
                self.assertEqual(value, 1)
            if key == 'email':
                self.assertEqual(value, self.__admin_credentials["email"])
            if key == 'f_name':
                self.assertEqual(value, self.__admin_credentials["f_name"])
            if key == 'l_name':
                self.assertEqual(value, self.__admin_credentials["l_name"])
            if key == 'is_admin':
                self.assertEqual(value, True)
            if key == 'is_staff':
                self.assertEqual(value, True)
            if key == 'is_active':
                self.assertEqual(value, True)

    def test_user_create(self):
        """
        Ensure we can create user using restAPI
        """
        data = json.dumps({
            "email": "simple@user.co",
            "password": "veryC0mpl3x$%",
            "f_name": "Simple",
            "l_name": "User"
        })
        content_type = "application/json"
        response = self.client.post(
            self.__users_list_url,
            data=data,
            content_type=content_type,
            HTTP_AUTHORIZATION=self.__auth
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        for key, value in response.data.items():
            if key == "id":
                # third user created so far
                self.assertEqual(value, 3)
            if key == "email":
                self.assertEqual(value, "simple@user.co")
            if key == "f_name":
                self.assertEqual(value, "Simple")
            if key == "l_name":
                self.assertEqual(value, "User")
            if key == "is_admin":
                self.assertEqual(value, False)
            if key == "is_staff":
                self.assertEqual(value, False)
            if key == "is_active":
                self.assertEqual(value, True)

    def test_get_user_with_valid_pk(self):
        """
        Ensure we can get a single user with valid pk
        """
        response = self.client.get(self.__user_detail_url, HTTP_AUTHORIZATION=self.__auth)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_with_invalid_pk(self):
        """
        Ensure we cannot get any user with an in-valid pk
        """
        url = reverse("user-accounts:user-detail", kwargs={"pk": 55})
        response = self.client.get(url, HTTP_AUTHORIZATION=self.__auth)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_edit_user_with_put(self):
        """
        Ensure we can edit a user using PUT method
        """
        data = {
            "f_name": "NewTest",
            "l_name": "User",
            "email": "test@user.co"
        }
        response = self.client.put(self.__user_detail_url, data=data, HTTP_AUTHORIZATION=self.__auth)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["f_name"], "NewTest")

    def test_edit_user_with_patch(self):
        """
        Ensure we can edit a user using PATCH method
        """
        data = {
            "f_name": "NewTest"
        }
        self.assertEqual(self.__test_user.f_name, "Test")
        response = self.client.patch(self.__user_detail_url, data=data, HTTP_AUTHORIZATION=self.__auth)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["f_name"], "NewTest")

    def test_delete_user(self):
        """
        Ensure we can delete user with DELETE method
        """
        self.assertEqual(User.objects.all().count(), 2)
        response = self.client.delete(self.__user_detail_url, HTTP_AUTHORIZATION=self.__auth)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data["detail"], "Delete success.")
        self.assertEqual(User.objects.all().count(), 1)

    def test_update_user_password(self):
        """
        Ensure we can update user password
        NOTE: Also, the API requests for updating password of requesting user
        So, password of superuser is used instead of test user. Its because, oauth token if
        made using admin user credentials.
        """
        data = {
            "password": "VeryComplex#$123",
            "new_password": "VerySimple#$321",
            "confirm_password": "VerySimple#$321"
        }
        response = self.client.post(self.__user_update_pw_url, data=data, HTTP_AUTHORIZATION=self.__auth)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data["detail"], "Update password success.")
        user = authenticate(email=self.__test_super_user, password=data["confirm_password"])
        self.assertIsNotNone(user)
        self.assertEqual(user.email, self.__admin_credentials["email"])
