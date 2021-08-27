from django.http import (
    JsonResponse,
    response,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import APIException
from rest_framework import status
from typing import (
    Generic,
    TypeVar,
)
SELFCLASS = TypeVar('SELFCLASS')
DEFAULT_DETAIL = {"error": "An error has ocurred."}
DEFAULT_CODE = status.HTTP_400_BAD_REQUEST


class CustomError(APIException):
    """Custom exception for any type of error generated in the applications."""

    def __new__(cls, detail: str = DEFAULT_DETAIL, code: status = DEFAULT_CODE, *args, **kwargs) -> Generic[SELFCLASS]:
        return super(CustomError, cls).__new__(cls, *args, **kwargs)

    def __init__(self, detail: dict = DEFAULT_DETAIL, code: status = DEFAULT_CODE) -> response:
        self.detail = detail
        self.status_code = code


class CustomTokenAuthentication(TokenAuthentication):
    """Exception is rewritten, for a custom error."""
    def authenticate_credentials(self, key: str) -> tuple:
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise CustomError(
                detail={'error': 'Invalid token.'}, code=401)

        if not token.user.is_active:
            raise CustomError(
                detail={'error': 'This account has been deactivated by an administrator.'}, code=401)

        return (token.user, token)


def http_404_not_found(request: any, exception: APIException) -> JsonResponse:
    message = ("The endpoint is not found.")

    response = JsonResponse(data={'error': message, 'status_code': 404})
    response.status_code = 404
    return response

def http_500_internal_server_error(request: any) -> JsonResponse:
    message = ("An error ocurred, it's on us.")

    response = JsonResponse(data={'error': message, 'status_code': 500})
    response.status_code = 500
    return response