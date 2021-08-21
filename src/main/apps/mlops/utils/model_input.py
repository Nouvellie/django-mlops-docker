import numpy as np

from typing import (
    Generic,
    List,
    TypeVar,
)
SelfClass = TypeVar('SelfClass')


class ModelInputGenerator:
    """Generate inputs for the Fashion Mnist model"""

    def __new__(cls, *args, **kwargs) -> Generic[SelfClass]:
        return super(ModelInputGenerator, cls).__new__(cls, *args, **kwargs)

    def __init__(self) -> None:
        pass

    def model_input_generator(self, model_input: np.ndarray) -> List:
        """Generates model input as an array."""
        model_input = np.expand_dims(np.array(model_input), axis=0)
        model_input = [model_input]
        return model_input
