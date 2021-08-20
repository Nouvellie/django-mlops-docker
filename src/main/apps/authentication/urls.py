from .views import (
    SignInAPI,
    SignUpAPI,
    TokenAPI,
    UserAPI,
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
]
