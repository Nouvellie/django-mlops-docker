from PIL import (
    Image,
    ImageFile,
)
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


class ImdbFileLoader:

    def __call__(self, model_input: str) -> str:
        try:
            model_input = model_input.read().decode("utf-8")
            return model_input
        except AttributeError:
            return model_input
        except :
            raise TypeError("Please send a review.")