import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from accounts.models import User


class UserTests(APITestCase):
    def setUp(self):
        User.objects.create_superuser(email='test@admin.co', password='admin', f_name='First', l_name='Last')

    def test_list_users(self):
        """
        Ensure we can list users created
        :return: void
        """
        client = APIClient()
        client.login(email='test@admin.co', password='admin')
        url = reverse('users-gc')
        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for key, value in response.data[0].items():
            if key == 'id':
                self.assertEqual(value, 1)
            if key == 'email':
                self.assertEqual(value, 'test@admin.co')
            if key == 'f_name':
                self.assertEqual(value, 'First')
            if key == 'l_name':
                self.assertEqual(value, 'Last')
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
        client = APIClient()
        client.login(email='test@admin.co', password='admin')
        url = reverse('users-gc')
        data = json.dumps({
            'email': 'test@user.co',
            'password': 'veryC0mpl3x$%',
            'f_name': 'Test',
            'l_name': 'User'
        })
        content_type = 'application/json'
        response = client.post(url, data=data, content_type=content_type)
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
