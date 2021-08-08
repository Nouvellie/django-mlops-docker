from .views import TFLiteFashionMnistAPIView
from django.urls import path


urlpatterns = [
	path(
        'tflite-fmnist',
        TFLiteFashionMnistAPIView.as_view(),
        name = 'tflite_fmnist',
    ),
]