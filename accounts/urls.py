from django.urls import path

from accounts.views.users import UserList, UserDetail
from accounts.views.login import LoginView
from accounts.views.password import UpdatePassword


urlpatterns = [
    path("user/login/", LoginView.as_view(), name='login'),
    path("users/", UserList.as_view(), name='users-list'),
    path("user/<int:pk>/", UserDetail.as_view(), name='user-detail'),
    path("user/update-password/", UpdatePassword.as_view(), name="update-pw"),
]
