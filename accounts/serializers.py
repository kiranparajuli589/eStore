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


class UpdatePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    @staticmethod
    def validate_new_password(password):
        validate_password(password)
        return password

    def validate(self, data):
        if data["new_password"] != data["confirm_password"]:
            raise serializers.ValidationError("New password must match with confirm password.")
        if data["confirm_password"] == data["password"]:
            raise serializers.ValidationError("New and old password must not be same.")
        return data


class ResetPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetNewPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    @staticmethod
    def validate_new_password(new_password):
        validate_password(new_password)
        return new_password

    def validate(self, data):
        if data["new_password"] != data["confirm_password"]:
            raise serializers.ValidationError("New password must match with confirm password.")
        return data
