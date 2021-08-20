from .serializers import (
    SignInSerializer,
    SignUpSerializer,
    UserInfoSerializer,
    UserSerializer,
)
from .token import (
    check_token,
    get_token,
    refresh_token,
)
from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    HTTP_426_UPGRADE_REQUIRED,
)


class SignUpAPI(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SignUpSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "credentials": UserSerializer(user, context=self.get_serializer_context()).data,
                "token": get_token(user),
            }, status=HTTP_201_CREATED)
        else:
            return Response({'error': serializer.errors,}, status=HTTP_400_BAD_REQUEST)


class SignInAPI(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SignInSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            return Response({
                "credentials": UserSerializer(user, context=self.get_serializer_context()).data,
                "token": refresh_token(user),
            }, status=HTTP_200_OK)
        else:
            return Response({'error': serializer.errors,}, status=HTTP_400_BAD_REQUEST)


class UserAPI(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SignInSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            return Response({
                "info": UserInfoSerializer(user, context=self.get_serializer_context()).data,
                "token": check_token(user),
            }, status=HTTP_200_OK)
        else:
            return Response({'error': serializer.errors,}, status=HTTP_400_BAD_REQUEST)


class TokenAPI(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = SignInSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            token_info = check_token(user)
            return Response({
                "token": token_info['token'],
                "info": token_info['info'],
            }, status=HTTP_200_OK)
        else:
            return Response({'error': serializer.errors,}, status=HTTP_400_BAD_REQUEST)
