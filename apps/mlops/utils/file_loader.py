import os

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
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

    def __call__(self, model_input: Generic[InMemoryUploadedFile]) -> Generic[PILImage]:
        model_input = Image.open(model_input)
        model_input = model_input.convert('L')
        return model_input


class ImdbSentimentFileLoader:

    def __call__(self, model_input: str) -> str:
        try:
            model_input = model_input.read().decode("utf-8")
            return model_input
        except AttributeError:
            return model_input
        except:
            raise TypeError("Please send a review.")


class StackoverflowFileLoader:

    def __call__(self, model_input: str) -> str:
        try:
            model_input = model_input.read().decode("utf-8")
            return model_input
        except AttributeError:
            return model_input
        except:
            raise TypeError("Please send a code.")


class CatsvsdogsFileLoader:

    def __call__(self, model_input: Generic[InMemoryUploadedFile]) -> Generic[PILImage]:
        path = default_storage.save(f"tmp/{model_input.name}", ContentFile(model_input.file.read()))
        model_input = os.path.join(settings.MEDIA_ROOT, path)
        # model_input = keras.preprocessing.image.load_img(
        #     model_input, target_size=(180,180)
        # )
        return model_input