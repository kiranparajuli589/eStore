from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from oauth2_provider.models import get_application_model
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.models import User, UserProfile
from accounts.permissions import IsAdminUser
from accounts.serializers import UserSerializer, UserCreateSerializer, UserUpdateSerializer

Application = get_application_model()


class UserList(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]

    @staticmethod
    @swagger_auto_schema(
        security=[{"Basic": []}],
        responses={
            status.HTTP_200_OK: openapi.Response(schema=UserSerializer, description="OK"),
            status.HTTP_403_FORBIDDEN: "Forbidden"
        }
    )
    def get(request):
        """
        List users
        """
        users = User.objects.all()
        return Response(UserSerializer(users, many=True).data, status=status.HTTP_200_OK)

    @staticmethod
    @swagger_auto_schema(
        security=[{"Basic": []}],
        request_body=UserCreateSerializer,
        responses={
            status.HTTP_201_CREATED: openapi.Response(schema=UserSerializer, description="OK"),
            status.HTTP_400_BAD_REQUEST: "Bad Request",
            status.HTTP_403_FORBIDDEN: "Forbidden"
        }
    )
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
            Application.objects.create(
                name="{} Application".format(user.f_name),
                redirect_uris="http://localhost",
                user=user,
                client_type=Application.CLIENT_CONFIDENTIAL,
                authorization_grant_type=Application.GRANT_PASSWORD,
            )
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    """
    User Detail API View
    """
    @staticmethod
    def get_object(pk):
        return get_object_or_404(User, pk=pk)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='id', in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="ID of a user instance.",
                required=True
            ),
        ],
        responses={
            status.HTTP_200_OK: UserSerializer,
            status.HTTP_400_BAD_REQUEST: "Bad Request",
            status.HTTP_403_FORBIDDEN: "Forbidden",
            status.HTTP_404_NOT_FOUND: "Not Found"
        }
    )
    def get(self, request, pk):
        """Retrieve a user instance."""
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='id', in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="ID of a user instance.",
                required=True
            ),
        ],
        request_body=UserUpdateSerializer,
        responses={
            status.HTTP_200_OK: openapi.Response(schema=UserUpdateSerializer, description="OK"),
            status.HTTP_400_BAD_REQUEST: "Bad Request",
            status.HTTP_403_FORBIDDEN: "Forbidden",
            status.HTTP_404_NOT_FOUND: "Not Found"
        }
    )
    def put(self, request, pk):
        """Modify a user instance"""
        user = self.get_object(pk)
        serializer = UserUpdateSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='id', in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="ID of a user instance.",
                required=True
            ),
        ],
        request_body=UserUpdateSerializer,
        responses={
            status.HTTP_200_OK: openapi.Response(schema=UserUpdateSerializer, description="OK"),
            status.HTTP_400_BAD_REQUEST: "Bad Request",
            status.HTTP_403_FORBIDDEN: "Forbidden",
            status.HTTP_404_NOT_FOUND: "Not Found"
        }
    )
    def patch(self, request, pk):
        """Modify a user instance"""
        user = self.get_object(pk)
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='id', in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="ID of a user instance.",
                required=True
            ),
        ],
        responses={
            status.HTTP_204_NO_CONTENT: openapi.Response(description="Delete success."),
            status.HTTP_400_BAD_REQUEST: "Bad Request",
            status.HTTP_403_FORBIDDEN: "Forbidden",
            status.HTTP_404_NOT_FOUND: "Not Found"
        }
    )
    def delete(self, request, pk):
        """Delete a user instance"""
        user = self.get_object(pk)
        user.delete()
        return Response({"detail": "Delete success."}, status=status.HTTP_204_NO_CONTENT)
