from django.test import TestCase
from .models import User


class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create_superuser(email='test@admin.co', password='admin')
        User.objects.create_staff_user(email='test@staff.co', password='staff')
        User.objects.create_user(email='test@user.co', password='test')
        User.objects.create(
            email='किरण@user.co', password='test',
            f_name='किरण', l_name='पराजुली'
        )

    def test_create_superuser(self):
        user = User.objects.get(email='test@admin.co')
        self.assertEqual(user.is_admin, True)
        self.assertEqual(user.is_staff, True)
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.phone, None)
        self.assertEqual(user.address, None)
        self.assertEqual(user.get_full_name(), None)
        self.assertEqual(user.upper_case_name(), None)

    def test_create_staff_user(self):
        user = User.objects.get(email='test@staff.co')
        self.assertEqual(user.is_admin, False)
        self.assertEqual(user.is_staff, True)
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.phone, None)
        self.assertEqual(user.address, None)
        self.assertEqual(user.get_full_name(), None)
        self.assertEqual(user.upper_case_name(), None)

    def test_create_user(self):
        user = User.objects.get(email='test@user.co')
        self.assertEqual(user.is_admin, False)
        self.assertEqual(user.is_staff, False)
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.phone, None)
        self.assertEqual(user.address, None)
        self.assertEqual(user.get_full_name(), None)
        self.assertEqual(user.upper_case_name(), None)

    def test_unicode_named_user(self):
        user = User.objects.get(email='किरण@user.co')
        self.assertEqual(user.f_name, 'किरण')
        self.assertEqual(user.l_name, 'पराजुली')
