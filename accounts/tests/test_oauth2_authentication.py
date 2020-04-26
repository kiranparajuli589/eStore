"""
OAuth2 verification test
These TestCases are also inside django-oauth-toolkit/tests/test_rest_framework
https://github.com/jazzband/django-oauth-toolkit/blob/e612c17adf03f7f21698b26386a500b137a0f7ee/tests/test_rest_framework.py
"""
from django.conf.urls import url
from django.http import HttpResponse
from django.test.utils import override_settings
from django.test import TestCase
from django.urls import include, reverse
from oauth2_provider.contrib.rest_framework import OAuth2Authentication, TokenHasScope
from oauth2_provider.settings import oauth2_settings
from rest_framework import permissions
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework.views import APIView

from accounts.models import User
from accounts.tests.helper.oauth_helper import OauthHelper


class MockView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        return HttpResponse({"message": "get request for mock view"})

    def post(self, request):
        return HttpResponse({"message": "post request for mock view"})

    def put(self, request):
        return HttpResponse({"message": "put request for mock view"})


class OAuth2View(MockView):
    authentication_classes = [OAuth2Authentication]


class ScopedView(OAuth2View):
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ["scope1"]


urlpatterns = [
    url(r"^oauth2/", include("oauth2_provider.urls")),
    url(r"^oauth2-test/$", OAuth2View.as_view(), name="oauth"),
    url(r"^oauth2-scoped-test/$", ScopedView.as_view(), name="scoped-oauth"),

]


@override_settings(ROOT_URLCONF=__name__)
class TestOAuth2Authentication(TestCase):
    def setUp(self):
        self.__regular_user_email = "test@regular.co"
        self.__password = "test"

        self.__test_regular_user = User.objects.create_user(
            email=self.__regular_user_email, password=self.__password,
            f_name="Test", l_name="Regular")
        self.oauth = OauthHelper()
        self.application = OauthHelper.get_application(self.oauth)
        self.access_token = OauthHelper.get_access_token(self.oauth)

    @staticmethod
    def create_authorization_header(token):
        return "Bearer {0}".format(token)

    def tearDown(self):
        oauth2_settings._SCOPES = ["read", "write"]

    def test_authentication_allow(self):
        auth = self.create_authorization_header(self.access_token.token)
        response = self.client.get("/oauth2-test/", HTTP_AUTHORIZATION=auth)
        self.assertEqual(response.status_code, 200)

    def test_authentication_denied(self):
        url = reverse("oauth")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response["WWW-Authenticate"],
            'Bearer realm="api"',
        )

    def test_authentication_denied_because_of_invalid_token(self):
        auth = self.create_authorization_header("fake-token")
        url = reverse("oauth")
        response = self.client.get(url, HTTP_AUTHORIZATION=auth)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response["WWW-Authenticate"],
            'Bearer realm="api",error="invalid_token",error_description="The access token is invalid."',
        )

    def test_authentication_or_scope_denied(self):
        # user not authenticated
        # not a correct token
        auth = self.create_authorization_header("fake-token")
        url = reverse("scoped-oauth")
        response = self.client.get(url, HTTP_AUTHORIZATION=auth)
        self.assertEqual(response.status_code, 401)
        # token doesn't have correct scope
        auth = self.create_authorization_header(self.access_token.token)

        factory = APIRequestFactory()
        request = factory.get(url)
        request.auth = auth
        force_authenticate(request, token=self.access_token.token)
        response = ScopedView.as_view()(request)
        # authenticated but wrong scope, this is 403, not 401
        self.assertEqual(response.status_code, 403)
