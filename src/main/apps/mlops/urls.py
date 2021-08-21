from .views import (
    TFLiteFashionMnist,
    HDF5JSONFashionMnist,

    TFLiteImdbSentiment,
    
    TFLiteStackoverflowAPIView,

    TFLiteCatsVsDogs,
    HDF5JSONCatsVsDogs,
)
from django.urls import path


urlpatterns = [

# FashionMnist.
    path(
        'tflite-fmnist',
        TFLiteFashionMnist.as_view(),
        name='tflite_fmnist',
    ),
    path(
        'hdf5json-fmnist',
        HDF5JSONFashionMnist.as_view(),
        name='hdf5json_fmnist',
    ),

# ImdbSentiment.
    path(
        'tflite-isentiment',
        TFLiteImdbSentiment.as_view(),
        name='tflite_isentiment',
    ),

# Stackoverflow
    path(
        'tflite-soverflow',
        TFLiteStackoverflowAPIView.as_view(),
        name='tflite_soverflow',
    ),

# CatsvsDogs
    path(
        'tflite-cvsdogs',
        TFLiteCatsVsDogs.as_view(),
        name='tflite_cvdogs',
    ),
    path(
        'hdf5json-cvsdogs',
        HDF5JSONCatsVsDogs.as_view(),
        name='hdf5json_cvdogs',
    ),
]
