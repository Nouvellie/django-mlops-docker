import numpy as np

from typing import List
# from .general_functions import from_json


class FashionMnistImageModelInput:
	"""Generate inputs for the Fashion Mnist model"""
	def __new__(cls, *args, **kwargs):
		return super(FashionMnistImageModelInput, cls).__new__(cls, *args, **kwargs)

	def __init__(self, model_input_from_json=None):
		self.model_input_from_json = model_input_from_json

	def fashionmnist_input(self, model_input: np.ndarray) -> List:
		model_input = np.expand_dims(np.array(model_input), axis=0)
		model_input = [model_input]
		return model_input