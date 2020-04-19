from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.models import User, UserProfile
from accounts.permissions import IsAdminPermission
from accounts.serializers import UserSerializer, UserCreateSerializer


class UserView(APIView):
    permission_classes = (IsAdminPermission, IsAuthenticated,)

    @staticmethod
    def get(request):
        """
        List users
        :param request
        :return: Response list of users created
        """
        users = User.objects.all()
        return Response(UserSerializer(users, many=True).data)

    @staticmethod
    def post(request):
        """
        Create user
        :param request
        :return: Response
        """
        serializer = UserCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(serializer.validated_data['password'])
            user.is_active = True
            user.save()
            UserProfile(user=user).save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
