from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from accounts.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'f_name', 'l_name', 'email', 'password',
                  'is_active', 'is_admin', 'is_staff',
                  'address', 'phone', 'email', 'date_created')

    @staticmethod
    def validate_password(password):
        validate_password(password)
        return password


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=64)
