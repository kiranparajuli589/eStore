from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from accounts.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "f_name", "l_name", "email", "password",
            "is_active", "is_admin", "is_staff", "address", "phone"
        )

    @staticmethod
    def validate_password(password):
        validate_password(password)
        return password


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("f_name", "l_name", "email", "address", "phone", "is_active", "is_staff", "is_admin")


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=64)
