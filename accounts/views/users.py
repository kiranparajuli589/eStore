from django.shortcuts import get_object_or_404
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from accounts.models import User, UserProfile
from accounts.permissions import IsAdminUser
from accounts.serializers import UserSerializer, UserCreateSerializer, UserUpdateSerializer


class UserList(APIView):
    permission_classes = [TokenHasReadWriteScope, permissions.IsAuthenticated, IsAdminUser]

    @staticmethod
    def get(request):
        """
        List users
        """
        users = User.objects.all()
        return Response(UserSerializer(users, many=True).data, status=status.HTTP_200_OK)

    @staticmethod
    def post(request):
        """
        Create user
        """
        serializer = UserCreateSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(serializer.validated_data["password"])
            user.is_active = True
            user.save()
            UserProfile(user=user).save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    """
    Retrieve, update or delete a user instance.
    """
    @staticmethod
    def get_object(pk):
        return get_object_or_404(User, pk=pk)

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        user = self.get_object(pk)
        serializer = UserUpdateSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        user = self.get_object(pk)
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_object(pk)
        email = user.email
        user.delete()
        return Response(
            {"detail": "User with email address {} deleted!".format(email)},
            status=status.HTTP_204_NO_CONTENT
        )
