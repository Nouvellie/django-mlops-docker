from .serializers import (
    FASHION_MNIST_HELP_TEXT,
    FashionMnistSerializer,

    IMDB_SENTIMENT_HELP_TEXT,
    ImdbSentimentSerializer,

    STACKOVERFLOW_HELP_TEXT,
    StackoverflowSerializer,

    CATS_VS_DOGS_HELP_TEXT,
    CatsVsDogsSerializer,
)
from .utils.model_loader import (
    CheckpointModelLoader,
    HDF5JSONModelLoader,
    TFLiteModelLoader,
)
from main.settings import (
    DEBUG,
    MODEL_ROOT,
)
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

######################## PRELOADED MODELS ########################

# ## FASHION MNIST ##
argmax_fashion_mnist_tflite_model = TFLiteModelLoader(
    model_dir="1/fashionmnist")
threshold_fashion_mnist_tflite_model = TFLiteModelLoader(
    model_dir="1/fashionmnist2")
argmax_fashion_mnist_hdf5json_model = HDF5JSONModelLoader(
    model_dir="1/fashionmnist")
threshold_fashion_mnist_hdf5json_model = HDF5JSONModelLoader(
    model_dir="1/fashionmnist2")

# ## IMDB SENTIMENT ##
argmax_imdb_sentiment_tflite_model = TFLiteModelLoader(
    model_dir="2/imdbsentiment")
threshold_imdb_sentiment_tflite_model = TFLiteModelLoader(
    model_dir="2/imdbsentiment2")
processed_argmax_imdb_sentiment_tflite_model = TFLiteModelLoader(
    model_dir="2/imdbsentiment3")

# ## STACKOVERFLOW ##
argmax_stackoverflow_tflite_model = TFLiteModelLoader(
    model_dir="3/stackoverflow")
threshold_stackoverflow_tflite_model = TFLiteModelLoader(
    model_dir="3/stackoverflow2")

## CATS VS DOGS ##
argmax_catsvsdogs_tflite_model = TFLiteModelLoader(
    model_dir="4/catsvsdogs")
threshold_catsvsdogs_tflite_model = TFLiteModelLoader(
    model_dir="4/catsvsdogs2")
argmax_catsvsdogs_hdf5json_model = HDF5JSONModelLoader(
    model_dir="4/catsvsdogs")
threshold_catsvsdogs_hdf5json_model = HDF5JSONModelLoader(
    model_dir="4/catsvsdogs2")


class TFLiteFashionMnist(GenericAPIView):
    """API for Fashion Mnist tflite model."""

    serializer_class = FashionMnistSerializer

    def post(self, request, format=None, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            model_input = serializer.validated_data['image']

            argmax_true_tflite_result = argmax_fashion_mnist_tflite_model.predict(
                model_input, confidence=True)
            argmax_false_tflite_result = argmax_fashion_mnist_tflite_model.predict(
                model_input)
            threshold_true_tflite_result = threshold_fashion_mnist_tflite_model.predict(
                model_input, confidence=True)
            threshold_false_tflite_result = threshold_fashion_mnist_tflite_model.predict(
                model_input)

            api_output = [{
                'argmax_true': argmax_true_tflite_result,
                'argmax_false': argmax_false_tflite_result,
                'threshold_true': threshold_true_tflite_result,
                'threshold_false': threshold_false_tflite_result, },
                HTTP_200_OK]
        else:
            api_output = [{'error': FASHION_MNIST_HELP_TEXT},
                          HTTP_400_BAD_REQUEST]
        return Response(api_output[0], status=api_output[1])

# from rest_framework.authentication import TokenAuthentication
class HDF5JSONFashionMnist(GenericAPIView):
    """API for Fashion Mnist hdf5json model."""

    serializer_class = FashionMnistSerializer

    def post(self, request, format=None, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            model_input = serializer.validated_data['image']

            argmax_true_hdf5json_result = argmax_fashion_mnist_hdf5json_model.predict(
                model_input, confidence=True)
            argmax_false_hdf5json_result = argmax_fashion_mnist_hdf5json_model.predict(
                model_input)
            threshold_true_hdf5json_result = threshold_fashion_mnist_hdf5json_model.predict(
                model_input, confidence=True)
            threshold_false_hdf5json_result = threshold_fashion_mnist_hdf5json_model.predict(
                model_input)

            api_output = [{
                'argmax_true': argmax_true_hdf5json_result,
                'argmax_false': argmax_false_hdf5json_result,
                'threshold_true': threshold_true_hdf5json_result,
                'threshold_false': threshold_false_hdf5json_result, },
                HTTP_200_OK]
        else:
            api_output = [{'error': FASHION_MNIST_HELP_TEXT},
                          HTTP_400_BAD_REQUEST]
        return Response(api_output[0], status=api_output[1])


class TFLiteImdbSentiment(GenericAPIView):
    """API for Imdb Sentiment tflite model."""

    serializer_class = ImdbSentimentSerializer

    def post(self, request, format=None, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            model_input = serializer.validated_data['review']

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

            api_output = [{
                'argmax_true': argmax_true_tflite_result,
                'argmax_false': argmax_false_tflite_result,
                'threshold_true': threshold_true_tflite_result,
                'threshold_false': threshold_false_tflite_result,
                'processed_argmax_true': processed_argmax_true_tflite_result, },
                HTTP_200_OK]
        else:
            api_output = [{'error': IMDB_SENTIMENT_HELP_TEXT},
                          HTTP_400_BAD_REQUEST]
        return Response(api_output[0], status=api_output[1])


class TFLiteStackoverflow(GenericAPIView):
    """API for StackOverFlow tflite model."""

    serializer_class = StackoverflowSerializer

    def post(self, request, format=None, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            model_input = serializer.validated_data['code']

            argmax_true_tflite_result = argmax_stackoverflow_tflite_model.predict(
                model_input, confidence=True)
            argmax_false_tflite_result = argmax_stackoverflow_tflite_model.predict(
                model_input)
            threshold_true_tflite_result = threshold_stackoverflow_tflite_model.predict(
                model_input, confidence=True)
            threshold_false_tflite_result = threshold_stackoverflow_tflite_model.predict(
                model_input)

            api_output = [{
                'argmax_true': argmax_true_tflite_result,
                'argmax_false': argmax_false_tflite_result,
                'threshold_true': threshold_true_tflite_result,
                'threshold_false': threshold_false_tflite_result, },
                HTTP_200_OK]
        else:
            api_output = [{'error': STACKOVERFLOW_HELP_TEXT},
                          HTTP_400_BAD_REQUEST]
        return Response(api_output[0], status=api_output[1])


class TFLiteCatsVsDogs(GenericAPIView):
    """API for Cats Vs Dogs tflite model."""

    serializer_class = CatsVsDogsSerializer

    def post(self, request, format=None, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            model_input = serializer.validated_data['image']

            argmax_true_tflite_result = argmax_catsvsdogs_tflite_model.predict(
                model_input, confidence=True)
            argmax_false_tflite_result = argmax_catsvsdogs_tflite_model.predict(
                model_input)
            threshold_true_tflite_result = threshold_catsvsdogs_tflite_model.predict(
                model_input, confidence=True)
            threshold_false_tflite_result = threshold_catsvsdogs_tflite_model.predict(
                model_input)

            api_output = [{
                'argmax_true': argmax_true_tflite_result,
                'argmax_false': argmax_false_tflite_result,
                'threshold_true': threshold_true_tflite_result,
                'threshold_false': threshold_false_tflite_result, },
                HTTP_200_OK]
        else:
            api_output = [{'error': CATS_VS_DOGS_HELP_TEXT},
                          HTTP_400_BAD_REQUEST]
        return Response(api_output[0], status=api_output[1])


class HDF5JSONCatsVsDogs(GenericAPIView):
    """API for Cats vs Dogs hdf5json model."""

    serializer_class = CatsVsDogsSerializer

    def post(self, request, format=None, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            model_input = serializer.validated_data['image']

            argmax_true_hdf5json_result = argmax_catsvsdogs_hdf5json_model.predict(
                model_input, confidence=True)
            argmax_false_hdf5json_result = argmax_catsvsdogs_hdf5json_model.predict(
                model_input)
            threshold_true_hdf5json_result = threshold_catsvsdogs_hdf5json_model.predict(
                model_input, confidence=True)
            threshold_false_hdf5json_result = threshold_catsvsdogs_hdf5json_model.predict(
                model_input)

            api_output = [{
                'argmax_true': argmax_true_hdf5json_result,
                'argmax_false': argmax_false_hdf5json_result,
                'threshold_true': threshold_true_hdf5json_result,
                'threshold_false': threshold_false_hdf5json_result, },
                HTTP_200_OK]
        else:
            api_output = [{'error': CATS_VS_DOGS_HELP_TEXT},
                          HTTP_400_BAD_REQUEST]
        return Response(api_output[0], status=api_output[1])
