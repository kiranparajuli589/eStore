from django.test import TestCase
from .models import User


class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create_superuser(email='test@admin.co', password='admin')
        User.objects.create_staff_user(email='test@staff.co', password='staff')
        User.objects.create_user(email='test@user.co', password='test')

    def test_create_superuser(self):
        user = User.objects.get(email='test@admin.co')
        self.assertEqual(user.is_admin, True)
        self.assertEqual(user.is_staff, True)
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.phone, None)
        self.assertEqual(user.address, None)

    def test_create_staff_user(self):
        user = User.objects.get(email='test@staff.co')
        self.assertEqual(user.is_admin, False)
        self.assertEqual(user.is_staff, True)
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.phone, None)
        self.assertEqual(user.address, None)

    def test_create_user(self):
        user = User.objects.get(email='test@user.co')
        self.assertEqual(user.is_admin, False)
        self.assertEqual(user.is_staff, False)
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.phone, None)
        self.assertEqual(user.address, None)
