from datetime import timedelta

from django.utils import timezone
from oauth2_provider.settings import oauth2_settings
from oauth2_provider.models import get_application_model, get_access_token_model

Application = get_application_model()
AccessToken = get_access_token_model()


class OauthHelper:
    def __init__(self, user, scope):
        """
        Sets up oauthClient for provided user
        :param user:User
        :param scope:array Array of scopes
        """
        oauth2_settings._SCOPES = scope
        self.application = Application.objects.create(
            name="Test Application",
            redirect_uris="http://localhost",
            user=user,
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_AUTHORIZATION_CODE,
        )
        self.access_token = AccessToken.objects.create(
            user=user,
            scope="read write",
            expires=timezone.now() + timedelta(seconds=300),
            token="secret-access-token-key",
            application=self.application
        )

    def get_application(self):
        return self.application

    def get_access_token(self):
        return self.access_token
