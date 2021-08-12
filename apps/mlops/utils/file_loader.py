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
        return model_input