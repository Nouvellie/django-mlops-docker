from datetime import (
    datetime,
    timedelta,
    timezone,
)
from rest_framework.authtoken.models import Token


def check_token(user):
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


def get_token(user):
    token, _ = Token.objects.get_or_create(user=user)
    return token.key


def refresh_token(user, refresh=True):
    Token.objects.filter(user=user).delete()
    token, _ = Token.objects.get_or_create(user=user)
    return token.key
