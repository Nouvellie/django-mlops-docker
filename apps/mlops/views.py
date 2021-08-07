import re
import traceback

from main.settings import DEBUG
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class FashionMnistAPIView(APIView):
	"""API for Fashion Mnist model."""

	def post(self, request, format=None):
		try:
			pass
		except:
			full_traceback = re.sub(r"\n\s*", " || ", traceback.format_exc())

			if DEBUG:
                return Response({'error': "bad_request", 'detail': full_traceback, }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': "bad_request",}, status=status.HTTP_400_BAD_REQUEST)
