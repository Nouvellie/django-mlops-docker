import numpy as np
import os

from .general_functions import ImdbSentimentTextModificator
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


@pipeline_function_register
def load_img(model_input: Any, target_size: Tuple = (180, 180)) -> Any:
    path_to_remove = str(model_input)
    model_input = keras.preprocessing.image.load_img(
        model_input, target_size=target_size
    )
    os.remove(path_to_remove)
    return model_input

@pipeline_function_register
def process_review_text(model_input: str, preprocess: bool = False) -> str:
    if preprocess:
        modificated_text = ImdbSentimentTextModificator(model_input)
        model_input = modificated_text.processed_review
    return model_input