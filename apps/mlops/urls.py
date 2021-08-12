from .views import (
    HDF5JSONFashionMnistAPIView,
    TFLiteFashionMnistAPIView,
    TFLiteImdbAPIView,
)
from django.urls import path


urlpatterns = [
    path(
        'hdf5json-fmnist',
        HDF5JSONFashionMnistAPIView.as_view(),
        name='hdf5json_fmnist',
    ),

    path(
        'tflite-fmnist',
        TFLiteFashionMnistAPIView.as_view(),
        name='tflite_fmnist',
    ),

    path(
        'tflite-imdb',
        TFLiteImdbAPIView.as_view(),
        name='tflite_imdb',
    ),
]
