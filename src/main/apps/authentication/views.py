from .serializers import SignUpSerializer, UserSerializer
from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED


# class SignUpView(GenericAPIView):

# 	serializer_class = SignUpSerializer

# 	def post(self, request, format=None):
# 		user = request.data
# 		serializer = self.serializer_class(data=user)
# 		serializer.is_valid(raise_exception=True)
# 		serializer.save()

# 		user_data = serializer.data

# 		return Response(user_data, status=HTTP_201_CREATED)


class SignUpView(GenericAPIView):
    serializer_class = SignUpSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
        })