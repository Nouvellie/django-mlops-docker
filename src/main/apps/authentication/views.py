from .email import send_email
from .serializers import (
	SignInSerializer,
	SignUpSerializer,
	UserInfoSerializer,
	UserSerializer,
)
from .token import (
	account_verification,
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
	HTTP_202_ACCEPTED,
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
			send_email(request, user)
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


class VerifyAPI(GenericAPIView):

	def post(self, request, format=None):
		try:
			send_email(request)
			return Response({'info': 'Email sent.'}, status=HTTP_200_OK)
		except:
			return Response({'error': 'There was a problem sending the email, try again in a moment.'}, status=HTTP_400_BAD_REQUEST)


class VerifyAccountAPI(GenericAPIView):
	permission_classes = (AllowAny,)

	def get(self, request):
		account_verified = account_verification(acc_hash=self.request.GET.get('verify'))

		if account_verified['status']:
			return Response({'info': 'Account successfully verified!'}, status=HTTP_202_ACCEPTED)
		elif not account_verified['status']:
			return Response({'error': account_verified['error']}, status=HTTP_400_BAD_REQUEST)
		else:
			return Response({'error': 'There was a problem sending the email, try again in a moment.'}, status=HTTP_400_BAD_REQUEST)
