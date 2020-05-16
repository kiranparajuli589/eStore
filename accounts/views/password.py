from django.contrib.auth import update_session_auth_hash, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from oauth2_provider.models import get_application_model, get_access_token_model

from accounts.models import User, ResetPasswordCode
from accounts.serializers import UpdatePasswordSerializer, ResetPasswordEmailSerializer, ResetNewPasswordSerializer
from backend import settings

Application = get_application_model()
AccessToken = get_access_token_model()


class UpdatePassword(APIView):
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
            if user:
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, request.user)
                return Response({"detail": "Update password success."}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"error": "Wrong existing password."}, status=status.HTTP_400_BAD_REQUEST)
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


class ResetPasswordRequest(APIView):
    permission_classes = ()
    authentication_classes = ()

    @staticmethod
    def post(request):
        """
        Reset user password -> Sends PIN to provided email address
        """
        serializer = ResetPasswordEmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            try:
                user = User.objects.get(email=email)

                current_site = get_current_site(request)
                code_object = ResetPasswordCode.objects.create(user=user)
                code = code_object.code
                mail_subject = "Reset user password"
                message = render_to_string("reset_email.html", {
                    "user": user.f_name,
                    "domain": current_site.domain,
                    "code": code,
                })
                send_mail(
                    mail_subject,
                    message="ResetPassword",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[email],
                    html_message=message
                )
                return Response({"detail": "PIN has been sent to provided mail address."}, status=status.HTTP_202_ACCEPTED)
            except User.DoesNotExist:
                return Response({"error": "User not found."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordConfirm(APIView):
    """
    Reset Password Confirm
    """
    permission_classes = ()
    authentication_classes = ()

    @staticmethod
    def post(request, code):
        serializer = ResetNewPasswordSerializer(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data["new_password"]
            try:
                reset_password_code = get_object_or_404(ResetPasswordCode, code=code)
                user = reset_password_code.user
                user.set_password(password)
                user.save()
                reset_password_code.delete()
                return Response({"detail": "Reset password success."}, status=status.HTTP_100_CONTINUE)
            except ResetPasswordCode.DoesNotExist:
                return Response({"error": "Code not found."})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
