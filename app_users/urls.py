from django.urls import path
from app_users.views import ChatUserRegisterView, UserLoginView, UserLogoutView

urlpatterns = [
    path(
        'register/',
        ChatUserRegisterView.as_view(),
        name='register',
    ),
    path(
        'login/',
        UserLoginView.as_view(),
        name='login',
    ),
    path(
        'logout/',
        UserLogoutView.as_view(),
        name='logout',
    ),
]
