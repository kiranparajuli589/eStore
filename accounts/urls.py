from django.urls import path
from accounts.views.views import UserView

urlpatterns = [
    path('user/', UserView.as_view(), name='users-gc')
]
