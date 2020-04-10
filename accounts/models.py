from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from datetime import datetime
import pytz

ktm = pytz.timezone('Asia/Kathmandu')
now = ktm.localize(datetime.now())


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('User must have a unique email address!!!')

        user = self.model(email=self.normalize_email(email=email))
        user.set_password(password)
        user.save()
        return user

    def create_staff_user(self, email, password=None):
        user = self.create_user(email, password=None)
        user.set_password(password)
        user.is_staff = True
        user.save()
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email, password=None)
        user.set_password(password)
        user.is_staff = True
        user.is_admin = True
        user.save()
        return user


class User(AbstractBaseUser):
    email = models.EmailField(unique=True, max_length=50, verbose_name='Email Address')
    f_name = models.CharField(max_length=50, verbose_name='First Name')
    l_name = models.CharField(max_length=50, verbose_name='Last Name')
    date_created = models.DateTimeField(default=now, verbose_name='Registered Date')

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def upper_case_name(obj):
        return ("%s %s" % (obj.f_name, obj.l_name)).upper()

    upper_case_name.short_description = 'Name'

    def get_full_name(self):
        return str(self.f_name + ' ' + self.l_name)

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, package_name):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

