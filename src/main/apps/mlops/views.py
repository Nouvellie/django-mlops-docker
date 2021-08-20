import os
import re
import time
import traceback

from .utils.model_loader import (
    CheckpointModelLoader,
    HDF5JSONModelLoader,
    TFLiteModelLoader,
)
from main.settings import (
    DEBUG,
    MODEL_ROOT,
)
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

######################## PRELOADED MODELS ########################

# ## FASHION MNIST ##
# argmax_fashion_mnist_tflite_model = TFLiteModelLoader(
#     model_dir="1/fashionmnist")
# threshold_fashion_mnist_tflite_model = TFLiteModelLoader(
#     model_dir="1/fashionmnist2")
# argmax_fashion_mnist_hdf5json_model = HDF5JSONModelLoader(
#     model_dir="1/fashionmnist")
# threshold_fashion_mnist_hdf5json_model = HDF5JSONModelLoader(
#     model_dir="1/fashionmnist2")

# ## IMDB SENTIMENT ##
# argmax_imdb_sentiment_tflite_model = TFLiteModelLoader(
#     model_dir="2/imdbsentiment")
# threshold_imdb_sentiment_tflite_model = TFLiteModelLoader(
#     model_dir="2/imdbsentiment2")
# processed_argmax_imdb_sentiment_tflite_model = TFLiteModelLoader(
#     model_dir="2/imdbsentiment3")

# ## STACKOVERFLOW ##
# argmax_stackoverflow_tflite_model = TFLiteModelLoader(
#     model_dir="3/stackoverflow")
# threshold_stackoverflow_tflite_model = TFLiteModelLoader(
#     model_dir="3/stackoverflow2")

# ## CATS VS DOGS ##
# argmax_catsvsdogs_tflite_model = TFLiteModelLoader(
#     model_dir="4/catsvsdogs")
# threshold_catsvsdogs_tflite_model = TFLiteModelLoader(
#     model_dir="4/catsvsdogs2")
# argmax_catsvsdogs_hdf5json_model = HDF5JSONModelLoader(
#     model_dir="4/catsvsdogs")
# threshold_catsvsdogs_hdf5json_model = HDF5JSONModelLoader(
#     model_dir="4/catsvsdogs2")


class TFLiteFashionMnistAPIView(APIView):
    """API for Fashion Mnist model."""

    def post(self, request, format=None):
        try:
            start_time = time.time()

            # If the api does not receive an image.
            if request.data.get('image') is None:
                return Response({'error': 'Please send an image.', }, status=status.HTTP_400_BAD_REQUEST)

            # If the image format is not png.
            # if not request.data['image'].name.endswith(".png"):
            #     return Response({'error': 'unsupported_media_type',}, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

            model_input = list(request.FILES.getlist('image'))[0]

            argmax_true_tflite_result = argmax_fashion_mnist_tflite_model.predict(
                model_input, confidence=True)
            argmax_false_tflite_result = argmax_fashion_mnist_tflite_model.predict(
                model_input)
            threshold_true_tflite_result = threshold_fashion_mnist_tflite_model.predict(
                model_input, confidence=True)
            threshold_false_tflite_result = threshold_fashion_mnist_tflite_model.predict(
                model_input)

            result = {
                'argmax_true': argmax_true_tflite_result,
                'argmax_false': argmax_false_tflite_result,
                'threshold_true': threshold_true_tflite_result,
                'threshold_false': threshold_false_tflite_result,
            }

            return Response(result, status=status.HTTP_200_OK)
        except:
            full_traceback = re.sub(r"\n\s*", " || ", traceback.format_exc())

            if DEBUG:
                return Response({'error': "bad_request", 'detail': full_traceback, }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': "bad_request", }, status=status.HTTP_400_BAD_REQUEST)


class HDF5JSONFashionMnistAPIView(APIView):
    """API for Fashion Mnist model."""

    def post(self, request, format=None):
        try:
            start_time = time.time()

            # If the api does not receive an image.
            if request.data.get('image') is None:
                return Response({'error': 'Please send an image.', }, status=status.HTTP_400_BAD_REQUEST)

            # If the image format is not png.
            # if not request.data['image'].name.endswith(".png"):
            #     return Response({'error': 'unsupported_media_type',}, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

            model_input = list(request.FILES.getlist('image'))[0]

            argmax_true_hdf5json_result = argmax_fashion_mnist_hdf5json_model.predict(
                model_input, confidence=True)
            argmax_false_hdf5json_result = argmax_fashion_mnist_hdf5json_model.predict(
                model_input)
            threshold_true_hdf5json_result = threshold_fashion_mnist_hdf5json_model.predict(
                model_input, confidence=True)
            threshold_false_hdf5json_result = threshold_fashion_mnist_hdf5json_model.predict(
                model_input)



            result = {
                'argmax_true': argmax_true_hdf5json_result,
                'argmax_false': argmax_false_hdf5json_result,
                'threshold_true': threshold_true_hdf5json_result,
                'threshold_false': threshold_false_hdf5json_result,
            }

            return Response(result, status=status.HTTP_200_OK)
        except:
            full_traceback = re.sub(r"\n\s*", " || ", traceback.format_exc())

            if DEBUG:
                return Response({'error': "bad_request", 'detail': full_traceback, }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': "bad_request", }, status=status.HTTP_400_BAD_REQUEST)


class TFLiteImdbSentimentAPIView(APIView):
    """API for Imdb Sentiment model."""

    def post(self, request, format=None):
        try:
            start_time = time.time()

            # If the api does not receive an image.
            if request.data.get('review') is None:
                return Response({'error': 'Please send a review.', }, status=status.HTTP_400_BAD_REQUEST)

            model_input = request.data.get('review')

            argmax_true_tflite_result = argmax_imdb_sentiment_tflite_model.predict(
                model_input, confidence=True)
            argmax_false_tflite_result = argmax_imdb_sentiment_tflite_model.predict(
                model_input)
            threshold_true_tflite_result = threshold_imdb_sentiment_tflite_model.predict(
                model_input, confidence=True)
            threshold_false_tflite_result = threshold_imdb_sentiment_tflite_model.predict(
                model_input)
            processed_argmax_true_tflite_result = processed_argmax_imdb_sentiment_tflite_model.predict(
                model_input, confidence=True)
            
            result = {
                'argmax_true': argmax_true_tflite_result,
                'argmax_false': argmax_false_tflite_result,
                'threshold_true': threshold_true_tflite_result,
                'threshold_false': threshold_false_tflite_result,
                'processed_argmax_true': processed_argmax_true_tflite_result,
            }

            return Response(result, status=status.HTTP_200_OK)
        except:
            full_traceback = re.sub(r"\n\s*", " || ", traceback.format_exc())

            if DEBUG:
                return Response({'error': "bad_request", 'detail': full_traceback, }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': "bad_request", }, status=status.HTTP_400_BAD_REQUEST)


class TFLiteStackoverflowAPIView(APIView):
    """API for StackOverFlow model."""

    def post(self, request, format=None):
        try:
            start_time = time.time()

            # If the api does not receive an image.
            if request.data.get('code') is None:
                return Response({'error': 'Please send a code.', }, status=status.HTTP_400_BAD_REQUEST)

            model_input = request.data.get('code')

            argmax_true_tflite_result = argmax_stackoverflow_tflite_model.predict(
                model_input, confidence=True)
            argmax_false_tflite_result = argmax_stackoverflow_tflite_model.predict(
                model_input)
            threshold_true_tflite_result = threshold_stackoverflow_tflite_model.predict(
                model_input, confidence=True)
            threshold_false_tflite_result = threshold_stackoverflow_tflite_model.predict(
                model_input)

            result = {
                'argmax_true': argmax_true_tflite_result,
                'argmax_false': argmax_false_tflite_result,
                'threshold_true': threshold_true_tflite_result,
                'threshold_false': threshold_false_tflite_result,
            }

            return Response(result, status=status.HTTP_200_OK)
        except:
            full_traceback = re.sub(r"\n\s*", " || ", traceback.format_exc())

            if DEBUG:
                return Response({'error': "bad_request", 'detail': full_traceback, }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': "bad_request", }, status=status.HTTP_400_BAD_REQUEST)


class TFLiteCatsvsdogsAPIView(APIView):
    """API for Cats vs Dogs model."""

    def post(self, request, format=None):
        try:
            start_time = time.time()

            # If the api does not receive an image.
            if request.data.get('image') is None:
                return Response({'error': 'Please send an image.', }, status=status.HTTP_400_BAD_REQUEST)

            model_input = list(request.FILES.getlist('image'))[0]

            argmax_true_tflite_result = argmax_catsvsdogs_tflite_model.predict(
                model_input, confidence=True)
            argmax_false_tflite_result = argmax_catsvsdogs_tflite_model.predict(
                model_input)
            threshold_true_tflite_result = threshold_catsvsdogs_tflite_model.predict(
                model_input, confidence=True)
            threshold_false_tflite_result = threshold_catsvsdogs_tflite_model.predict(
                model_input)

            result = {
                'argmax_true': argmax_true_tflite_result,
                'argmax_false': argmax_false_tflite_result,
                'threshold_true': threshold_true_tflite_result,
                'threshold_false': threshold_false_tflite_result,
            }

            return Response(result, status=status.HTTP_200_OK)
        except:
            full_traceback = re.sub(r"\n\s*", " || ", traceback.format_exc())

            if DEBUG:
                return Response({'error': "bad_request", 'detail': full_traceback, }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': "bad_request", }, status=status.HTTP_400_BAD_REQUEST)


class HDF5JSONCatsvsdogsAPIView(APIView):
    """API for Cats vs Dogs model."""

    def post(self, request, format=None):
        try:
            start_time = time.time()

            # If the api does not receive an image.
            if request.data.get('image') is None:
                return Response({'error': 'Please send an image.', }, status=status.HTTP_400_BAD_REQUEST)

            model_input = list(request.FILES.getlist('image'))[0]

            argmax_true_hdf5json_result = argmax_catsvsdogs_hdf5json_model.predict(
                model_input, confidence=True)
            argmax_false_hdf5json_result = argmax_catsvsdogs_hdf5json_model.predict(
                model_input)
            threshold_true_hdf5json_result = threshold_catsvsdogs_hdf5json_model.predict(
                model_input, confidence=True)
            threshold_false_hdf5json_result = threshold_catsvsdogs_hdf5json_model.predict(
                model_input)

            result = {
                'argmax_true': argmax_true_hdf5json_result,
                'argmax_false': argmax_false_hdf5json_result,
                'threshold_true': threshold_true_hdf5json_result,
                'threshold_false': threshold_false_hdf5json_result,
            }

            return Response(result, status=status.HTTP_200_OK)
        except:
            full_traceback = re.sub(r"\n\s*", " || ", traceback.format_exc())

            if DEBUG:
                return Response({'error': "bad_request", 'detail': full_traceback, }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': "bad_request", }, status=status.HTTP_400_BAD_REQUEST)
