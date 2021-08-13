import numpy as np

from typing import List


class ModelInputGenerator:
    """Generate inputs for the Fashion Mnist model"""
    def __new__(cls, *args, **kwargs):
        return super(ModelInputGenerator, cls).__new__(cls, *args, **kwargs)

    def __init__(self, model_input_from_json=None):
        self.model_input_from_json = model_input_from_json

    def model_input_generator(self, model_input: np.ndarray) -> List:
        model_input = np.expand_dims(np.array(model_input), axis=0)
        model_input = [model_input]
        return model_input
