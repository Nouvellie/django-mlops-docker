from .views import (
    VerifyAPI,
    SignInAPI,
    SignUpAPI,
    TokenAPI,
    UserAPI,
    VerifyAccountAPI,
)
from django.urls import path


urlpatterns = [
    path(
        'signup',
        SignUpAPI.as_view(),
        name='signup',
    ),
    path(
        'signin',
        SignInAPI.as_view(),
        name='signin',
    ),
    path(
        'token',
        TokenAPI.as_view(),
        name='token',
    ),
    path(
        'user',
        UserAPI.as_view(),
        name='user_info',
    ),
    path(
        'verify-account',
        VerifyAccountAPI.as_view(),
        name='verify_account',
    ),
    path(
        'verify',
        VerifyAPI.as_view(),
        name='verify',
    ),
]
