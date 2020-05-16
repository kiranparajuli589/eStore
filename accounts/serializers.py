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
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text="Type old password",
        style={"input_type": "password", "placeholder": "Old Password"}
    )
    new_password = serializers.CharField(
        write_only=True,
        required=True,
        help_text="Type new password",
        style={"input_type": "password", "placeholder": "New Password"}
    )
    confirm = serializers.CharField(
        write_only=True,
        required=True,
        help_text="Confirm new password",
        style={"input_type": "password", "placeholder": "Confirm New Password"}
    )

    @staticmethod
    def validate_new_password(password):
        validate_password(password)
        return password

    def validate(self, data):
        if data["new_password"] != data["confirm"]:
            raise serializers.ValidationError("New password must match with confirm password.")
        if data["confirm"] == data["password"]:
            raise serializers.ValidationError("New and old password must not be same.")
        return data
