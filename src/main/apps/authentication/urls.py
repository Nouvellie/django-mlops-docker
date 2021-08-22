from .views import (
    SignIn,
    SignUp,
    TokenInfoOut,
    UserInfoIn,
    UserInfoOut,
    VerifyAPI,
    VerifyAccountAPI,
)
from django.urls import path


urlpatterns = [

# SignUp:
    path(
        'signup',
        SignUp.as_view(),
        name='signup',
    ),
# SignIn:
    path(
        'signin',
        SignIn.as_view(),
        name='signin',
    ),

# INFO:
    path(
        'user-info-in',
        UserInfoIn.as_view(),
        name='user_info_in',
    ),
    path(
        'user-info-out',
        UserInfoOut.as_view(),
        name='user_info_out',
    ),
    path(
        'token-info-out',
        TokenInfoOut.as_view(),
        name='token_out',
    ),

# ACCOUNT MANAGEMENT:
    path(
        'verify',
        VerifyAPI.as_view(),
        name='verify',
    ),
    path(
        'verify-account',
        VerifyAccountAPI.as_view(),
        name='verify_account',
    ),
]
