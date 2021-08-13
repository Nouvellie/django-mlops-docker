import numpy as np

from .pipeline import pipeline_function_register
from tensorflow import keras
from typing import (
    Any,
    List,
    Tuple,
)


@pipeline_function_register
def resize_img(model_input: Any, target_size: Tuple = (28, 28)) -> Any:
    return model_input.resize(target_size)


@pipeline_function_register
def rescale_img(model_input: Any, factor: float = 255.0) -> Any:
    """Scale these values to a range of 0 to 1 before feeding them to the neural network model."""
    return np.array(model_input)/factor


@pipeline_function_register
def img_to_array(model_input: Any) -> Any:
    model_input = keras.preprocessing.image.img_to_array(model_input)
    return model_input