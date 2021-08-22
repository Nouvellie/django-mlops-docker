from .views import (
    SignInAPI,
    SignUpAPI,
    TokenAPI,
    UserAPI,
    VerifyAPI,
    VerifyAccountAPI,
)
from django.urls import path


urlpatterns = [

# SignUp:
    path(
        'signup',
        SignUpAPI.as_view(),
        name='signup',
    ),
# SignIn:
    path(
        'signin',
        SignInAPI.as_view(),
        name='signin',
    ),

# INFO:
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

# ACCOUNT MANAGEMENT:
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
