import re
import time
import traceback

from .utils.model_loader import TFLiteModelLoader
from main.settings import (
    DEBUG,
    MODEL_ROOT,
)
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

# Preloaded models.
fashion_mnist_tflite_model = TFLiteModelLoader(model_dir="1/fashionmnist")


class FashionMnistAPIView(APIView):
    """API for Fashion Mnist model."""

    def post(self, request, format=None):
        try:
            start_time = time.time()

            # If the api does not receive an image.
            if request.data.get('image') is None:
                return Response({'error': 'Please send an image.',}, status=status.HTTP_400_BAD_REQUEST)

            # If the image format is not png.
            # if not request.data['image'].name.endswith(".png"):
            #     return Response({'error': 'unsupported_media_type',}, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

            model_input = list(request.FILES.getlist('image'))[0]

            tflite_result = fashion_mnist_tflite_model.predict(model_input)

            return Response(status=status.HTTP_200_OK)
        except:
            full_traceback = re.sub(r"\n\s*", " || ", traceback.format_exc())

            if DEBUG:
                return Response({'error': "bad_request", 'detail': full_traceback, }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': "bad_request", }, status=status.HTTP_400_BAD_REQUEST)
