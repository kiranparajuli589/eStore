from datetime import timedelta

from django.utils import timezone
from oauth2_provider.settings import oauth2_settings
from oauth2_provider.models import get_application_model, get_access_token_model

from accounts.models import User

Application = get_application_model()
AccessToken = get_access_token_model()


class OauthHelper:
    def __init__(self):
        oauth2_settings._SCOPES = ["read", "write", "test"]
        self._admin_user_email = "test@admin.co"
        self._password = "test"
        self._admin_f_name = "Test"
        self._admin_l_name = "Admin"
        self._test_admin_user = User.objects.create_superuser(
            email=self._admin_user_email,
            password=self._password,
            f_name=self._admin_f_name,
            l_name=self._admin_l_name
        )
        self.application = Application.objects.create(
            name="Test Application",
            redirect_uris="http://localhost",
            user=self._test_admin_user,
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_AUTHORIZATION_CODE,
        )
        self.access_token = AccessToken.objects.create(
            user=self._test_admin_user,
            scope="read write",
            expires=timezone.now() + timedelta(seconds=300),
            token="secret-access-token-key",
            application=self.application
        )

    def get_application(self):
        return self.application

    def get_access_token(self):
        return self.access_token

    def get_admin_credentials(self):
        return dict({
            "email": self._admin_user_email,
            "password": self._password,
            "f_name": self._admin_f_name,
            "l_name": self._admin_l_name
        })
