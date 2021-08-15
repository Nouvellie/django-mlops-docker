import os

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from PIL import (
    Image,
    ImageFile,
)
from main.settings import MEDIA_ROOT
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

    def __call__(self, model_input: Generic[InMemoryUploadedFile]) -> Generic[PILImage]:
        model_input = Image.open(model_input)
        model_input = model_input.convert('L')
        return model_input


class ImdbSentimentFileLoader:

    def __call__(self, model_input: str) -> str:
        try:
            model_input = model_input.open().read().decode("utf-8")
            return model_input
        except AttributeError:
            return model_input
        except:
            raise TypeError("Please send a review.")


class StackoverflowFileLoader:

    def __call__(self, model_input: str) -> str:
        try:
            model_input = model_input.open().read().decode("utf-8")
            return model_input
        except AttributeError:
            return model_input
        except:
            raise TypeError("Please send a code.")


class CatsvsdogsFileLoader:

    def __call__(self, model_input: Generic[InMemoryUploadedFile]) -> str:
        path = default_storage.save(f"tmp/{model_input.name}", ContentFile(model_input.file.read()))
        model_input.file.seek(0)
        model_input = os.path.join(MEDIA_ROOT, path)
        return model_input
