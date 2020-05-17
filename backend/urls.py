"""
backend URL Configuration
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

swagger_info = openapi.Info(
    title="iStore API Documentation",
    default_version="v1",
    description="""This is an `API documentation` for the [iStore](https://github.com/kiranparajuli589/eStore) Django Rest Framework project.

The `swagger-ui` view can be found [here](/cached/swagger).
The `ReDoc` view can be found [here](/cached/redoc).
The `swagger YAML` document can be found [here](/cached/swagger.yaml).

You can log in using the pre-existing `admin@test.com` user with password `admin`.""",  # noqa
    terms_of_service="https://www.google.com/policies/terms/",
    contact=openapi.Contact(email="test@kiran.local"),
    license=openapi.License(name="BSD License"),
)

SchemaView = get_schema_view(
    validators=["ssv", "flex"],
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    url(r"^swagger(?P<format>\.json|\.yaml)$", SchemaView.without_ui(cache_timeout=0), name="schema-json"),
    url(r"^swagger/$", SchemaView.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    url(r"^redoc/$", SchemaView.with_ui("redoc", cache_timeout=0), name="schema-redoc"),

    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("o/", include("oauth2_provider.urls", namespace="oauth2_provider")),
    path("api/v1/accounts/", include("accounts.urls", namespace="user-accounts")),
]
