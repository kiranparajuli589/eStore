from django.test import TestCase
from accounts.models import User


class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create_superuser(email='test@admin.co', password='admin', f_name='Admin', l_name='User')
        User.objects.create_staff_user(email='test@staff.co', password='staff', f_name='Staff', l_name='User')
        User.objects.create_user(email='test@user.co', password='test', f_name='Test', l_name='User')
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
        self.assertEqual(user.get_full_name(), 'Admin User')
        self.assertEqual(user.upper_case_name(), 'ADMIN USER')

    def test_create_staff_user(self):
        user = User.objects.get(email='test@staff.co')
        self.assertEqual(user.is_admin, False)
        self.assertEqual(user.is_staff, True)
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.phone, None)
        self.assertEqual(user.address, None)
        self.assertEqual(user.get_full_name(), 'Staff User')
        self.assertEqual(user.upper_case_name(), 'STAFF USER')

    def test_create_user(self):
        user = User.objects.get(email='test@user.co')
        self.assertEqual(user.is_admin, False)
        self.assertEqual(user.is_staff, False)
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.phone, None)
        self.assertEqual(user.address, None)
        self.assertEqual(user.get_full_name(), 'Test User')
        self.assertEqual(user.upper_case_name(), 'TEST USER')

    def test_unicode_named_user(self):
        user = User.objects.get(email='किरण@user.co')
        self.assertEqual(user.f_name, 'किरण')
        self.assertEqual(user.l_name, 'पराजुली')
