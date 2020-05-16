from django.contrib.auth import update_session_auth_hash, authenticate
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, OAuth2Authentication
from oauth2_provider.models import get_application_model, get_access_token_model

from accounts.serializers import UpdatePasswordSerializer

Application = get_application_model()
AccessToken = get_access_token_model()


class UpdatePassword(APIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    authentication_classes = [OAuth2Authentication]

    @staticmethod
    def post(request):
        """
        Update password for authenticated user
        """
        serializer = UpdatePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            password = serializer.validated_data["password"]
            new_password = serializer.validated_data["new_password"]
            user = authenticate(email=request.user.email, password=password)
            print(user)
            if user:
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, request.user)
                return Response({"detail": "Update password success."}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"detail": "Wrong existing password."}, status=status.HTTP_400_BAD_REQUEST)
            # """
            # User must have access_token to access this api
            # After password is changed, lets change access_token too.
            # """
            # application = Application.objects.get(user=user, name=user.f_name)
            # access_token = AccessToken.objects.get(user=user)
            # refresh_token = access_token.refresh_token
            # request_token_url = "http://{}{}".format(iSTORE_SERVER_URL, reverse('oauth2_provider:token'))
            # data = {
            #     "grant_type": "refresh_token",
            #     "refresh_token": refresh_token,
            # }
            # token_response = requests.post(
            #     url=request_token_url,
            #     data=data,
            #     auth=(application.client_id, application.client_secret)
            # )
            # token_response_content = json.loads(token_response.content.decode("utf-8"))
            # return Response({"detail": "Update password success."},
            #                 status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
