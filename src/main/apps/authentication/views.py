from .email import send_email
from .serializers import (
    AccountVerificationSerializer,
    SignInSerializer,
    SignUpSerializer,
    UserInfoSerializer,
    UserSerializer,
    TokenInfoSerializer,
)
from .token import (
    account_verification,
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
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_426_UPGRADE_REQUIRED,
)
from rest_framework.views import APIView


class SignUp(GenericAPIView):
    """Api for account creation, and an automatic email to verify the account."""

    permission_classes = (AllowAny,)
    serializer_class = SignUpSerializer

    def post(self, request, format=None, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            send_email(request=request, user=user, thread=True)
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
    """Api that sends a link to the user's email to validate the account."""

    serializer_class = TokenInfoSerializer

    def get(self, request, format=None, *args, **kwargs):
        try:
            send_email(request=request, user=request.user, thread=False)
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
            regex = re.compile("[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}\Z", re.I)
            if not bool(regex.match(acc_hash)):
                return Response({'error': "The verification link is invalid, please request a new one."}, status=HTTP_403_FORBIDDEN)
            serializer = serializer = self.get_serializer(data={'acc_hash': acc_hash})
            if serializer.is_valid(raise_exception=True):
                return Response({'info': 'Account successfully verified!'}, status=HTTP_202_ACCEPTED)
        else:
            return Response({'error': 'The account must be verified with the link sent to the following e-mail address.'}, status=HTTP_400_BAD_REQUEST)
