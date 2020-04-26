from django.urls import path

from accounts.views.users import UserList, UserDetail
from accounts.views.login import LoginView


urlpatterns = [
    path("user/login/", LoginView.as_view(), name='login'),
    path("users/", UserList.as_view(), name='users-list'),
    path("user/<int:pk>/", UserDetail.as_view(), name='user-detail'),
]
