from datetime import datetime
import pytz
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from PIL import Image
from phonenumber_field.modelfields import PhoneNumberField

KTM = pytz.timezone('Asia/Kathmandu')
NOW = KTM.localize(datetime.now())


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


class Actor(models.Model):
    f_name = models.CharField(max_length=50, verbose_name='First Name')
    l_name = models.CharField(max_length=50, verbose_name='Last Name')

    address = models.CharField(max_length=50, null=True, blank=True)
    phone = PhoneNumberField(region='NP')
    email = models.EmailField(unique=True, max_length=50, verbose_name='Email Address', blank=True, null=True)
    date_created = models.DateTimeField(default=NOW, verbose_name='Date of Registration')

    class Meta:
        abstract = True
        ordering = ['f_name']

    def __str__(self):
        return "{} {}".format(self.f_name, self.l_name)


class User(AbstractBaseUser, Actor):
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def get_full_name(self):
        return '{} {}'.format(self.f_name, self.l_name)

    def upper_case_name(self):
        return self.get_full_name().upper()
    upper_case_name.short_description = 'Name'

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, package_name):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    user_avatar = models.ImageField(default='default.png',
                                    upload_to='profile_avatar',
                                    blank=True,
                                    verbose_name='Profile Avatar')

    class Meta:
        verbose_name_plural = "User Profiles"

    def __str__(self):
        return '{} Profile'.format(self.user.get_full_name())

    def save(self, **kwargs):
        super().save()
        img = Image.open(self.user_avatar.path)
        if img.height > 500 or img.width > 500:
            output_size = (500, 500)
            img.thumbnail(output_size)
            img.save(self.user_avatar.path)

    def get_user_address(self):
        return self.user.address
    get_user_address.short_description = 'Address'

    def get_user_phone(self):
        return self.user.phone
    get_user_phone.short_description = 'Phone Number'


class Vendor(Actor):
    tot_due = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    tot_received = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    image = models.ImageField(default='vendor-default.png', upload_to='vendor', verbose_name='Image(Vendor)')

    class Meta:
        verbose_name_plural = "Vendors"

    def save(self, **kwargs):
        super().save()

        img = Image.open(self.image.path)
        if img.height > 500 or img.width > 500:
            output_size = (500, 500)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def get_vendor_name(self):
        return "{} {}".format(self.f_name, self.l_name)
    get_vendor_name.short_description = 'Vendors'


class Customer(Actor):
    tot_due = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    tot_received = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    image = models.ImageField(default='customer-default.png', upload_to='customer', verbose_name='Image(Customer)')

    class Meta:
        verbose_name_plural = "Customers"

    def save(self, **kwargs):
        super().save()

        img = Image.open(self.image.path)
        if img.height > 500 or img.width > 500:
            output_size = (500, 500)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def get_customer_name(self):
        return "{} {}".format(self.f_name, self.l_name)
    get_customer_name.short_description = 'Customers'
