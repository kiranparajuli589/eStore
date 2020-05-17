from django.contrib.auth import authenticate
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from accounts.serializers import UserSerializer, LoginSerializer


class LoginView(APIView):
    authentication_classes = ()
    permission_classes = ()

    @staticmethod
    @swagger_auto_schema(
        security=[],
        request_body=LoginSerializer,
        responses={
            status.HTTP_202_ACCEPTED: openapi.Response(description="Login success."),
            status.HTTP_400_BAD_REQUEST: openapi.Response(description="Bad request"),
            status.HTTP_404_NOT_FOUND: "User not found"
        }
    )
    def post(request):
        """
        Login a user instance
        """
        serializer = LoginSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            email = serializer.data['email']
            password = serializer.data['password']
            try:
                User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"detail": "User not found!"}, status=status.HTTP_404_NOT_FOUND)
            user = authenticate(username=email, password=password)
            if user:
                serializer = UserSerializer(user)
                # TODO: create_or_refresh token
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            return Response(
                {"detail": "Password doesn't match!"},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
