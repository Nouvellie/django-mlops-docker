from .models import User
from datetime import (
    datetime,
    timedelta,
    timezone,
)
from rest_framework.authtoken.models import Token
from typing import Dict


def check_token(user: User) -> Token:
    """This function verifies the token, its validity and expiration."""
    token_status = {}
    token_status['info'] = {}
    token, _ = Token.objects.get_or_create(user=user)
    timenow = datetime.now(timezone.utc)
    token_status['token'] = token.key
    token_status['info']['created'] = token.created.strftime(
        ("%m/%d/%Y %H:%M:%S"))
    token_status['info']['expiration'] = token.created + \
        timedelta(days=365.25/4)
    token_status['info']['expiration'] = token_status['info']['expiration'].strftime(
        ("%m/%d/%Y %H:%M:%S"))
    token_status['info']['date_format'] = "MM/DD/YYYY HH:MM:SS"

    if token.created < (timenow - timedelta(days=365.25/4)):
        token_status['info']['message'] = 'Token has expired.'
    else:
        token_status['info']['message'] = 'Token still valid.'
    return token_status


def get_token(user: User) -> Token:
    """This function returns only the token of the queried user."""
    token, _ = Token.objects.get_or_create(user=user)
    return token.key


def refresh_token(user, refresh: bool = True) -> Token:
    """This function returns a refreshed token of the queried user."""
    Token.objects.filter(user=user).delete()
    token, _ = Token.objects.get_or_create(user=user)
    return token.key


def account_verification(acc_hash: str) -> Dict:
    """This function receives the verification sent to the email, processes it and, if it is correct, validates the account."""
    account_verified = {}
    account_verified['status'] = False
    print("jeje")
    user = User.objects.get(acc_hash=acc_hash)
    print("jaja",user)

    if not user.is_active:
        account_verified['error'] = 'This account cannot be verified because it has been deactivated by an administrator.'
    elif user.is_verified:
        account_verified['error'] = 'This account has already been verified.'
    else:
        user.is_verified = True
        user.save()
        account_verified['status'] = True

    return account_verified
