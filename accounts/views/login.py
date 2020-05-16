from django.contrib.auth import authenticate
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
            email = serializer.data['email']
            password = serializer.data['password']
            try:
                User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"detail": "User not found!"}, status=status.HTTP_404_NOT_FOUND)
            user = authenticate(username=email, password=password)
            if user:
                serializer = UserSerializer(user)
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            return Response(
                {"detail": "Password doesn't match!"},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
