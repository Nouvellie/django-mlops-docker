from main.exceptions import CustomError
from rest_framework import serializers
from rest_framework.exceptions import (
    UnsupportedMediaType,
    ValidationError,
    ErrorDetail
)
from typing import (
    Generic,
    TypeVar,
)
API_INPUTS = TypeVar('API_INPUTS')

# HELP TEXT.
FASHION_MNIST_HELP_TEXT = f"Please enter an image to process with FashionMnist model. The filename cannot be longer than 50 characters and only .png format will be accepted."
IMDB_SENTIMENT_HELP_TEXT = f"Please enter a file or text (review) to be processed with the Imdb Sentiment model. The filename cannot be longer than 50 characters and the allowed formats are '.md, .txt, .docx'. (In case both parameters are sent, the file is validated first and only one is answered.)"
STACKOVERFLOW_HELP_TEXT = f"Please enter a file or text (code) to be processed with the Stackoverflow model. The filename cannot be longer than 50 characters and the allowed formats are '.md, .txt, .docx'. (In case both parameters are sent, the file is validated first and only one is answered.)"
CATS_VS_DOGS_HELP_TEXT = f"Please enter an image to process with CatsVsDogs model. The filename cannot be longer than 50 characters and only .jpg format will be accepted."


class FashionMnistSerializer(serializers.Serializer):
    """Returns a serialized dictionary for the Fashion Mnist model."""

    image = serializers.FileField(
        required=True,
        write_only=True,
        help_text=FASHION_MNIST_HELP_TEXT,
        label="Image",
        max_length=50,
        use_url=False,
    )

    class Meta:
        fields = ('image',)

    def validate(self, attrs: Generic[API_INPUTS]) -> Generic[API_INPUTS]:
        """Validates if the input is an image and in .png format."""
        media_type = attrs.get('image').name.split(".")[-1]
        if not media_type.endswith("png"):
            raise CustomError(
                detail={'error': "Only .png format will be accepted."}, code=415)
        return super().validate(attrs)


class ImdbSentimentSerializer(serializers.Serializer):
    """Returns a serialized dictionary for the Imdb Sentiment model."""

    file = serializers.FileField(
        required=False,
        write_only=True,
        help_text=IMDB_SENTIMENT_HELP_TEXT,
        label="File",
        max_length=50,
        use_url=False,
    )
    text = serializers.CharField(
        required=False,
        write_only=True,
        help_text=IMDB_SENTIMENT_HELP_TEXT,
        label="Text",
        trim_whitespace=True,
    )

    class Meta:
        fields = ('file', 'text')

    def validate(self, attrs: Generic[API_INPUTS]) -> Generic[API_INPUTS]:
        """Validates if the input is a file or text and in .docx .txt .md format."""
        if attrs.get('file'):
            media_type = attrs.get('file').name.split(".")[-1]
            if not media_type.endswith(('docx', 'txt', 'md')):
                if not attrs.get('text'):
                    raise CustomError(
                        detail={'error': "Only '.doc .txt or .md' format will be accepted."}, code=415)
                else:
                    attrs.update({'review': attrs.get('text')})
            else:
                attrs.update({'review': attrs.get('file')})
        elif not attrs.get('file') and attrs.get('text'):
            attrs.update({'review': attrs.get('text')})
        elif not attrs.get('file') and not attrs.get('text'):
            raise CustomError(
                detail={'error': "You must send at least one. (text or file)"}, code=400)
        return super().validate(attrs)


class StackoverflowSerializer(serializers.Serializer):
    """Returns a serialized dictionary for the Stackoverflow model."""

    file = serializers.FileField(
        required=False,
        write_only=True,
        help_text=STACKOVERFLOW_HELP_TEXT,
        label="File",
        max_length=50,
        use_url=False,
    )
    text = serializers.CharField(
        required=False,
        write_only=True,
        help_text=STACKOVERFLOW_HELP_TEXT,
        label="Text",
        trim_whitespace=False,
    )

    class Meta:
        fields = ('file', 'text',)

    def validate(self, attrs: Generic[API_INPUTS]) -> Generic[API_INPUTS]:
        """Validates if the input is a file or text and in .docx .txt .md format."""
        if attrs.get('file'):
            media_type = attrs.get('file').name.split(".")[-1]
            if not media_type.endswith(('docx', 'txt', 'md')):
                if not attrs.get('text'):
                    raise CustomError(
                        detail={'error': "Only '.doc .txt or .md' format will be accepted."}, code=415)
                else:
                    attrs.update({'code': attrs.get('text')})
            else:
                attrs.update({'code': attrs.get('file')})
        elif not attrs.get('file') and attrs.get('text'):
            attrs.update({'code': attrs.get('text')})
        elif not attrs.get('file') and not attrs.get('text'):
            raise CustomError(
                detail={'error': "You must send at least one. (text or file)"}, code=400)
        return super().validate(attrs)


class CatsVsDogsSerializer(serializers.Serializer):
    """Returns a serialized dictionary for the Cats Vs Dogs model."""

    image = serializers.FileField(
        required=True,
        write_only=True,
        help_text=CATS_VS_DOGS_HELP_TEXT,
        label="Image",
        max_length=50,
        use_url=False,
    )

    class Meta:
        fields = ('image',)

    def validate(self, attrs: Generic[API_INPUTS]) -> Generic[API_INPUTS]:
        """Validates if the input is an image and in .jpg format."""
        media_type = attrs.get('image').name.split(".")[-1]
        if not media_type.endswith("jpg"):
            raise CustomError(
                detail={'error': "Only .jpg format will be accepted."}, code=415)
        return super().validate(attrs)
