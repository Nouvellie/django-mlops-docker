from .views import (
    HDF5JSONCatsvsdogsAPIView,
    HDF5JSONFashionMnistAPIView,
    TFLiteCatsvsdogsAPIView,
    TFLiteFashionMnistAPIView,
    TFLiteImdbSentimentAPIView,
    TFLiteStackoverflowAPIView,
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
        'tflite-isentiment',
        TFLiteImdbSentimentAPIView.as_view(),
        name='tflite_isentiment',
    ),

    path(
        'tflite-soverflow',
        TFLiteStackoverflowAPIView.as_view(),
        name='tflite_soverflow',
    ),

    path(
        'tflite-cvsdogs',
        TFLiteCatsvsdogsAPIView.as_view(),
        name='tflite_cvdogs',
    ),

    path(
        'hdf5json-cvsdogs',
        HDF5JSONCatsvsdogsAPIView.as_view(),
        name='hdf5json_cvdogs',
    ),
]
