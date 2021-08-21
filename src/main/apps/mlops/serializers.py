from rest_framework import serializers
from rest_framework.exceptions import UnsupportedMediaType
from typing import (
    Generic,
    TypeVar,
)
API_INPUTS = TypeVar('API_INPUTS')

# HELP TEXT.
FASHION_MNIST_HELP_TEXT = f"Please enter an image to process with FashionMnist model. The filename cannot be longer than 50 characters and only .png format will be accepted."


class FashionMnistSerializer(serializers.Serializer):
	"""Returns a serialized dictionary for the Fashion Mnist model."""

	image = serializers.FileField(
		required=True,
		write_only=True,
		help_text=FASHION_MNIST_HELP_TEXT,
		label="Image",
		max_length=50,
		use_url=False,
		allow_empty_file=False,
	)

	class Meta:
		fields = ('image',)

	def validate(self, attrs: Generic[API_INPUTS]) -> Generic[API_INPUTS]:
		"""Validates if the input is an image and in png format."""
		media_type = attrs.get('image').name.split(".")[-1]
		if not media_type.endswith("png"):
			raise UnsupportedMediaType(media_type=media_type, detail="Only .png format will be accepted")
		return super().validate(attrs)