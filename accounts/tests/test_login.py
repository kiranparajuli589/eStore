from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User


class LoginTest(APITestCase):
    def setUp(self):
        self._user_email = "test@user.com"
        self._user_password = "test"
        self._user_f_name = "Regular"
        self._user_l_name = "User"
        User.objects.create_user(
            email=self._user_email,
            f_name=self._user_f_name,
            l_name=self._user_l_name,
            password=self._user_password
        )
        self._url = reverse("login")

    def test_login_success_with_valid_user_credentials(self):
        """
        Ensure successful login with valid credentials
        """
        data = {
            "email": self._user_email,
            "password": self._user_password,
        }
        response = self.client.post(self._url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(response.data["email"], self._user_email)

    def test_login_failure_with_invalid_email_address(self):
        """
        Ensure login failure with in-valid email-address
        """
        data = {
            "email": "fake@user.com",
            "password": self._user_password,
        }
        response = self.client.post(self._url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], "Not found.")

    def test_login_failure_with_valid_email_but_invalid_password(self):
        """
        Ensure login failure with valid email address but invalid password
        """
        data = {
            "email": self._user_email,
            "password": "fake",
        }
        response = self.client.post(self._url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], "Password doesn't match!")

    def test_login_required_parameters(self):
        required_message = "This field is required."
        data = {}
        response = self.client.post(self._url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["email"][0], required_message)
        self.assertEqual(response.data["password"][0], required_message)
        data = {
            "email": self._user_email
        }
        response = self.client.post(self._url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["password"][0], required_message)
        data = {
            "password": self._user_password
        }
        response = self.client.post(self._url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["email"][0], required_message)
