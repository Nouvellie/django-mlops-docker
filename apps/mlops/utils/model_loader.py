import numpy as np
import os
import re
import traceback

from .file_loader import (
    FashionMnistFileLoader,
    ImdbSentimentFileLoader,
    StackoverflowFileLoader,
)
from .model_input import ModelInputGenerator
from .output_decoder import OutputDecoder
from .pipeline import Pipeline
from .preprocessing import pipeline_function_register
from abc import (
    ABC,
    abstractmethod,
)
from main.settings import (
    DEBUG,
    MODEL_ROOT,
)
from tensorflow import (
    convert_to_tensor,
    lite,
)
from tensorflow.keras.models import model_from_json
from typing import (
    Any,
    Dict,
    List,
)


class BaseModelLoader(ABC):
    """Metaclass for defining the model loader."""

    def __new__(cls, model_dir: str, *args, **kwargs):
        return super(BaseModelLoader, cls).__new__(cls, *args, **kwargs)

    def __init__(self, model_dir: str):
        self.model_type = int(model_dir.split("/")[0])
        self.model_dir = model_dir
        self.model_preload()
        self.preprocessing_load()
        self.postprocessing_load()
        self.model_input_load()
        self.preload_file_loader()

    def preprocessing_load(self):
        """Function to apply preprocessing to an array."""
        preprocessing_path = os.path.join(MODEL_ROOT + f"{self.model_dir}/preprocessing.json")

        self.preprocessing = Pipeline()
        self.preprocessing.from_json(preprocessing_path)

    def postprocessing_load(self):
        """Function to apply postprocessing to model output."""
        postprocessing_path = os.path.join(MODEL_ROOT + f"{self.model_dir}/postprocessing.json")

        self.postprocessing = OutputDecoder()
        self.postprocessing.from_json(postprocessing_path)

    def model_input_load(self):
        self.ModelInput = ModelInputGenerator()

    def preload_file_loader(self):
        """Function to load the file as an array."""
        if self.model_type == 1:
            self.file_loader = FashionMnistFileLoader()
        elif self.model_type == 2:
            self.file_loader = ImdbSentimentFileLoader()
        elif self.model_type == 3:
            self.file_loader = StackoverflowFileLoader()
        else:
            pass

    def generate_model_input(self, model_input: Any) -> List:
        """From file -> array -> preprocessing -> model input."""
        model_input = self.file_loader(model_input)
        model_input = self.preprocessing(model_input)
        model_input = self.ModelInput.model_input_generator(model_input)
        return model_input

    @abstractmethod
    def model_preload(self):
        pass

    @abstractmethod
    def predict(self):
        pass


class TFLiteModelLoader(BaseModelLoader):
    """Class to generate predictions from a TFLite model"""
    NUM_THREADS = 4

    def model_preload(self):
        tflite_name = [name for name in os.listdir(MODEL_ROOT + f"{self.model_dir}") if name.endswith(".tflite")][0]
        model_path = os.path.join(MODEL_ROOT + f"{self.model_dir}/{tflite_name}")

        if self.NUM_THREADS > 0:
            self.interpreter = lite.Interpreter(
                model_path=str(model_path), num_threads=self.NUM_THREADS)
        else:
            self.interpreter = lite.Interpreter(model_path=str(model_path))

        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        # print(f"The model {self.model_dir.title()} has been successfully pre-loaded. (TFLITE)")

    def predict(self, model_input: Any, confidence: bool = False) -> Dict:
        try:
            model_input = self.generate_model_input(model_input)

            if self.model_type == 1:
                for i, j in enumerate(model_input):
                    model_input_tensor = convert_to_tensor(np.array(j), np.float32)
                    self.interpreter.set_tensor(
                        self.input_details[i]['index'], model_input_tensor)

            elif self.model_type in (2, 3):
                for i, j in enumerate(model_input):
                    self.interpreter.set_tensor(
                        self.input_details[i]['index'], j)

            self.interpreter.invoke()

            prediction = self.interpreter.get_tensor(
                self.output_details[0]['index'])
            result = self.postprocessing.output_decoding(
                model_output=prediction, confidence=confidence)
            return result
        except Exception as e:
            if DEBUG:
                full_traceback = re.sub(
                    r"\n\s*", " || ", traceback.format_exc())
                print(full_traceback, e)


class HDF5JSONModelLoader(BaseModelLoader):
    """Class to generate predictions from a HDF5JSON model"""

    def model_preload(self):
        hdf5_path = os.path.join(MODEL_ROOT + f"{self.model_dir}/model.hdf5")
        json_path = os.path.join(MODEL_ROOT + f"{self.model_dir}/model.json")

        with open(json_path, "r") as jp:
            self.model = model_from_json(jp.read())
        self.model.load_weights(hdf5_path)
        # print(f"The model {self.model_dir.title()} has been successfully pre-loaded. (HDF5-JSON)")

    def predict(self, model_input: Any, confidence: bool = False) -> Dict:
        try:
            model_input = self.generate_model_input(model_input)

            prediction = self.model.predict(model_input)
            result = self.postprocessing.output_decoding(
                model_output=prediction, confidence=confidence)
            return result
        except Exception as e:
            if DEBUG:
                full_traceback = re.sub(
                    r"\n\s*", " || ", traceback.format_exc())
                print(full_traceback, e)
