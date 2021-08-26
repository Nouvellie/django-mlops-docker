import re

from .email import send_email
from .models import User
from .serializers import (
    AccountVerificationSerializer,
    PasswordResetSerializer,
    SignInSerializer,
    SignUpSerializer,
    UserInfoSerializer,
    UserSerializer,
    TokenInfoSerializer,
)
from .token import (
    check_token,
    get_token,
    refresh_token,
)
from rest_framework.generics import (
    GenericAPIView,
    RetrieveAPIView,
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_202_ACCEPTED,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
)


class SignUp(GenericAPIView):
    """Api for account creation, and an automatic email to verify the account."""

    permission_classes = (AllowAny,)
    serializer_class = SignUpSerializer

    def post(self, request, format=None, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            send_email(request=request, user=user, thread=True, task=1)
            return Response({
                "credentials": UserSerializer(user, context=self.get_serializer_context()).data,
                "token": get_token(user),
            }, status=HTTP_201_CREATED)
        else:
            return Response({'error': serializer.errors, }, status=HTTP_400_BAD_REQUEST)


class SignIn(GenericAPIView):
    """Api for signin, which in turn refreshes the current token."""

    permission_classes = (AllowAny,)
    serializer_class = SignInSerializer

    def post(self, request, format=None, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.get_user()
            return Response({
                "credentials": UserSerializer(user, context=self.get_serializer_context()).data,
                "token": refresh_token(user),
            }, status=HTTP_200_OK)
        else:
            return Response({'error': serializer.errors, }, status=HTTP_400_BAD_REQUEST)


class UserInfoOut(GenericAPIView):
    """Api that displays relevant user information. (token included)"""

    permission_classes = (AllowAny,)
    serializer_class = SignInSerializer

    def post(self, request, format=None, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.get_user()
            return Response({
                "info": UserInfoSerializer(user, context=self.get_serializer_context()).data,
                "token": check_token(user),
            }, status=HTTP_200_OK)
        else:
            return Response({'error': serializer.errors, }, status=HTTP_400_BAD_REQUEST)


class UserInfoIn(RetrieveAPIView):
    """Api that displays relevant user information. (token included)"""

    serializer_class = TokenInfoSerializer

    def get(self, request, format=None, *args, **kwargs):
        user_info = {
            "info": UserInfoSerializer(request.user, context=self.get_serializer_context()).data,
            "token": check_token(request.user),
        }
        return Response(user_info, status=HTTP_200_OK)


class TokenInfoOut(GenericAPIView):
    """Api that displays relevant information of each user's token."""

    permission_classes = (AllowAny,)
    serializer_class = SignInSerializer

    def post(self, request, format=None, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.get_user()
            token_info = check_token(user)
            return Response({
                "token": token_info['token'],
                "info": token_info['info'],
            }, status=HTTP_200_OK)
        else:
            return Response({'error': serializer.errors, }, status=HTTP_400_BAD_REQUEST)


class TokenInfoIn(RetrieveAPIView):
    """Api that displays relevant information of each user's token."""

    serializer_class = TokenInfoSerializer

    def get(self, request, format=None, *args, **kwargs):
        token_info = check_token(request.user)
        return Response(token_info, status=HTTP_200_OK)


class Verify(GenericAPIView):
    """Api that sends a link to the user's email to validate their account."""

    permission_classes = (AllowAny,)
    serializer_class = TokenInfoSerializer

    def get(self, request, format=None, *args, **kwargs):
        user = User.objects.get(username=request.user)
        if user.is_verified and user.is_active:
            return Response({'info': 'This account has already been verified.'}, status=HTTP_202_ACCEPTED)
        if not user.is_active:
            return Response({'info': 'This account cannot be verified because it has been deactivated by an administrator.'}, status=HTTP_403_FORBIDDEN)
        try:
            send_email(request=request, user=request.user,
                       thread=False, task=1)
            return Response({'info': 'Email sent.'}, status=HTTP_200_OK)
        except:
            return Response({'error': 'There was a problem sending the email, try again in a moment.'}, status=HTTP_400_BAD_REQUEST)


class AccountVerification(GenericAPIView):
    """This api receives the verification link sent to the email, processes it and, if it is correct, validates the account."""

    permission_classes = (AllowAny,)
    serializer_class = AccountVerificationSerializer

    def get(self, request, format=None, *args, **kwargs):
        acc_hash = self.request.GET.get('verify')
        if acc_hash:
            regex = re.compile(
                "[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}\Z", re.I)
            if not bool(regex.match(acc_hash)):
                return Response({'error': "The verification link is invalid, please request a new one."}, status=HTTP_403_FORBIDDEN)
            serializer = serializer = self.get_serializer(
                data={'acc_hash': acc_hash})
            if serializer.is_valid(raise_exception=True):
                return Response({'info': 'Account successfully verified!'}, status=HTTP_202_ACCEPTED)
        else:
            return Response({'error': 'The account must be verified with the link sent to the registered email address.'}, status=HTTP_400_BAD_REQUEST)


class PasswordResetRequest(GenericAPIView):
    """Api that sends a link to the user's email to reset his password."""

    serializer_class = TokenInfoSerializer

    def get(self, request, format=None, *args, **kwargs):
        user = User.objects.get(username=request.user)
        if user.is_verified and user.is_active:
            try:
                send_email(request=request, user=request.user,
                           thread=False, task=2)
                return Response({'info': 'Email sent.'}, status=HTTP_200_OK)
            except:
                return Response({'error': 'There was a problem sending the email, try again in a moment.'}, status=HTTP_400_BAD_REQUEST)    
        elif not user.is_active:
            return Response({'info': 'This account cannot be verified because it has been deactivated by an administrator.'}, status=HTTP_403_FORBIDDEN)
        elif not user.is_verified:
            return Response({'info': 'This account has not been verified.'}, status=HTTP_403_FORBIDDEN)


class PasswordReset(GenericAPIView):
    """API to change the password using a temporary token."""

    permission_classes = (AllowAny,)
    serializer_class = PasswordResetSerializer

    def get(self, request, format=None, *args, **kwargs):
        pass_token = self.request.GET.get('token')
        password = self.request.GET.get('password')
        if pass_token and password:
            regex = re.compile(
                "[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}\Z", re.I)
            if not bool(regex.match(pass_token)):
                return Response({'error': "The password reset link is invalid, please request a new one."}, status=HTTP_403_FORBIDDEN)
            serializer = serializer = self.get_serializer(
                data={'pass_token': pass_token, 'password': password})
            if serializer.is_valid(raise_exception=True):
                return Response({'info': 'Password successfully reset!'}, status=HTTP_202_ACCEPTED)
        if not password:
            return Response({'error': 'The new password must be sent.'}, status=HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'The password must be reset with the link sent to the registered email address.'}, status=HTTP_400_BAD_REQUEST)
