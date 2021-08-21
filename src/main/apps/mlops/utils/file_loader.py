import os

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from docx import Document
from main.settings import MEDIA_ROOT
from PIL import (
    Image,
    ImageFile,
)
from tensorflow import keras
from typing import (
    Generic,
    TypeVar,
)

# Some extra settings.
ImageFile.LOAD_TRUNCATED_IMAGES = True
InMemoryUploadedFile = TypeVar('InMemoryUploadedFile')
PILImage = TypeVar('PILImage')


class FashionMnistFileLoader:
    """Preloading of inputs (mostly files) from the FashionMnist API."""

    def __call__(self, model_input: Generic[InMemoryUploadedFile]) -> Generic[PILImage]:
        model_input = Image.open(model_input)
        model_input = model_input.convert('L')
        return model_input


class ImdbSentimentFileLoader:
    """Preloading of inputs (mostly files) from the ImdbSentiment API."""

    def __call__(self, model_input: str) -> str:
        try:
            if model_input.name.endswith('.docx'):
                model_input = Document(model_input).paragraphs[0].text
            elif model_input.name.endswith(('.txt', 'md')):
                model_input = model_input.open().read()
            return model_input
        except AttributeError:
            return model_input
        except:
            raise TypeError("Please send a review.")


class StackoverflowFileLoader:
    """Preloading of inputs (mostly files) from the Stackoverflow API."""

    def __call__(self, model_input: str) -> str:
        try:
            model_input = model_input.open().read().decode("utf-8")
            return model_input
        except AttributeError:
            return model_input
        except:
            raise TypeError("Please send a code.")


class CatsvsdogsFileLoader:
    """Preloading of inputs (mostly files) into the Catsvsdogs API."""

    def __call__(self, model_input: Generic[InMemoryUploadedFile]) -> str:
        path = default_storage.save(f"tmp/{model_input.name}", ContentFile(model_input.file.read()))
        model_input.file.seek(0)
        model_input = os.path.join(MEDIA_ROOT, path)
        return model_input
