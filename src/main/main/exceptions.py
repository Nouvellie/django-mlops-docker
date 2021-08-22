from django.http import response
from rest_framework.exceptions import APIException
from rest_framework import status
from typing import (
    Generic,
    TypeVar,
)
SELFCLASS = TypeVar('SELFCLASS')
DEFAULT_DETAIL = "An error has ocurred"
DEFAULT_CODE = status.HTTP_400_BAD_REQUEST


class CustomError(APIException):
    """Custom exception for any type of error generated in the applications."""

    def __new__(cls, detail: str = DEFAULT_DETAIL, code: status = DEFAULT_CODE, *args, **kwargs) -> Generic[SELFCLASS]:
        return super(CustomError, cls).__new__(cls, *args, **kwargs)

    def __init__(self, detail: str = DEFAULT_DETAIL, code: status = DEFAULT_CODE) -> response:
        self.detail = {'error': detail}
        self.status_code = code
