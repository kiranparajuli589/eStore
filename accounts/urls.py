from django.urls import path

from accounts.views.users import UserView
from accounts.views.login import LoginView

urlpatterns = [
    path('user/', UserView.as_view(), name='users-gc'),
    path('user/login/', LoginView.as_view(), name='login'),
]
