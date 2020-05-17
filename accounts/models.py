import uuid
from datetime import datetime
import pytz
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from PIL import Image
from phonenumber_field.modelfields import PhoneNumberField

KTM = pytz.timezone("Asia/Kathmandu")
NOW = KTM.localize(datetime.now())
IMAGE_OUTPUT_SIZE = (500, 500)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def __create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError("email address field is required!")
        if not password:
            raise ValueError("password field is required!")
        if "f_name" not in kwargs.keys():
            raise ValueError("first name field is required!")
        if "l_name" not in kwargs.keys():
            raise ValueError("last name field is required!")

        email = self.normalize_email(email)
        is_staff = kwargs.pop("is_staff", False)
        is_admin = kwargs.pop("is_admin", False)
        user = self.model(
            email=email,
            is_active=True,
            is_staff=is_staff,
            is_admin=is_admin,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self.__create_user(email, password, **extra_fields)

    def create_staff_user(self, email, password=None, **extra_fields):
        return self.__create_user(email, password, is_staff=True, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(email, password, is_staff=True, is_admin=True, **extra_fields)
        user.is_staff = True
        user.is_admin = True
        user.save()
        return user


class Actor(models.Model):
    f_name = models.CharField(max_length=50, verbose_name="First Name")
    l_name = models.CharField(max_length=50, verbose_name="Last Name")

    address = models.CharField(max_length=50, null=True, blank=True)
    phone = PhoneNumberField(region="NP", blank=True, null=True, unique=True, verbose_name="Phone Number")
    email = models.EmailField(unique=True, max_length=50, verbose_name="Email Address")
    date_created = models.DateTimeField(default=NOW, verbose_name="Date of Registration")

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

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "f_name",
        "l_name",
    ]

    class Meta:
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email

    def get_full_name(self):
        if self.f_name and self.l_name:
            return "{} {}".format(self.f_name, self.l_name)
        else:
            return None

    def upper_case_name(self):
        if self.f_name and self.l_name:
            return self.get_full_name().upper()
        else:
            return None
    upper_case_name.short_description = "Name"

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, package_name):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True


class ResetPasswordCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)

    class Meta:
        verbose_name_plural = "Reset Password Codes"

    def __str__(self):
        return "{} - {}".format(self.user.email, self.code)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    user_avatar = models.ImageField(default="default.png",
                                    upload_to="profile_avatar",
                                    blank=True,
                                    verbose_name="Profile Avatar")

    class Meta:
        verbose_name_plural = "User Profiles"

    @property
    def __str__(self):
        return "{} Profile".format(self.user.get_full_name())

    def save(self, **kwargs):
        super().save()
        img = Image.open(self.user_avatar.path)
        if img.height > 500 or img.width > 500:
            img.resize(IMAGE_OUTPUT_SIZE, Image.BILINEAR)
            img.save(self.user_avatar.path)

    def get_user_address(self):
        return self.user.address
    get_user_address.short_description = "Address"

    def get_user_phone(self):
        return self.user.phone
    get_user_phone.short_description = "Phone Number"


class Vendor(Actor):
    tot_due = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    tot_received = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    image = models.ImageField(default="vendor-default.png", upload_to='vendors', verbose_name="Image(Vendor)")

    class Meta:
        verbose_name_plural = "Vendors"

    def save(self, **kwargs):
        super().save()

        img = Image.open(self.image.path)
        if img.height > 500 or img.width > 500:
            img.resize(IMAGE_OUTPUT_SIZE, Image.BILINEAR)
            img.save(self.image.path)

    def get_vendor_name(self):
        return "{} {}".format(self.f_name, self.l_name)
    get_vendor_name.short_description = "Vendors"


class Customer(Actor):
    tot_due = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    tot_received = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    image = models.ImageField(default="customer-default.png", upload_to="customers", verbose_name="Image(Customer)")

    class Meta:
        verbose_name_plural = "Customers"

    def save(self, **kwargs):
        super().save()

        img = Image.open(self.image.path)
        if img.height > 500 or img.width > 500:
            img.resize(IMAGE_OUTPUT_SIZE, Image.BILINEAR)
            img.save(self.image.path)

    def get_customer_name(self):
        return "{} {}".format(self.f_name, self.l_name)
    get_customer_name.short_description = "Customers"
