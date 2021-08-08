from .views import FashionMnistAPIView
from django.urls import path


urlpatterns = [
	path(
        'fmnist',
        FashionMnistAPIView.as_view(),
        name = 'fmnist',
    ),
]