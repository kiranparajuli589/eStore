from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from accounts.serializers import UserSerializer, LoginSerializer


class LoginView(APIView):
    authentication_classes = ()
    permission_classes = ()

    @staticmethod
    def post(request):
        """
        Get user data and authenticate
        :param request: http request
        :return: Response
        """
        serializer = LoginSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = get_object_or_404(User, email=request.data.get('email'))
            user = authenticate(username=user.email, password=request.data.get('password'))
            if user:
                serializer = UserSerializer(user)
                print(serializer.data)
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "Wrong credentials provided!"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
