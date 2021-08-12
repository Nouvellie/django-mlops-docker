import json
import numpy as np

from math import floor
from pathlib import Path
from typing import (
    Dict,
    List,
    Optional,
    Union,
)


class OutputDecoder:
    """
    Decode the output of a model. Get the predicted classes using 'argmax' or 'threshold'.

    argmax=True -> threshold is not use

    If you want to load a postprocess from a json file, instantiate the class with no parameters
    >> decoder = OutputDecoder()
    >> decoder.from_json(path_postprocessing="path/to/postprocessing.json")

    Otherwise, provide inputs for:

    Multiclass (many outputs, one choice)
    >> decoder = OutputDecoder(ordered_model_output = ["class1", "class2", "class3"], argmax = True)

    Using the threshold for each class: (if prediction[class]>threshold then return 1, otherwise return 0)
    >> decoder = OutputDecoder(ordered_model_output = ["class1", "class2", "class3"], threshold = 0.5)
    """

    def __new__(cls, ordered_model_output: Optional[List[str]] = None, argmax: bool = False, threshold: Optional[Union[float, List[float]]] = None, *args, **kwargs):
        return super(OutputDecoder, cls).__new__(cls, *args, **kwargs)

    def __init__(self, ordered_model_output: Optional[List[str]] = None, argmax: bool = False, threshold: Optional[Union[float, List[float]]] = None):
        self.ordered_model_output = ordered_model_output
        self.decode_output_by = 'argmax' if argmax is True else 'threshold'
        self.threshold = threshold
        self.decoder_config()

    def decoder_config(self):
        self.config = dict(
            ordered_model_output=self.ordered_model_output,
            decode_output_by=self.decode_output_by,
            threshold=self.threshold
        )

    def decode_by_argmax(self, list_output: List[float]) -> List:
        """Output decoding via argmax."""
        return [self.ordered_model_output[np.argmax(list_output)]]

    def decode_by_threshold(self, list_output: List[float]) -> List:
        """Output decoding via threshold."""
        if isinstance(self.threshold, list):
            assert len(self.threshold) == len(
                self.ordered_model_output), 'The list of thresholds does not have the same length as the output'
            return [class_ for class_, pred, threshold in zip(self.ordered_model_output, list_output, self.threshold) if pred >= threshold]
        elif isinstance(self.threshold, float):
            return [class_ for class_, pred in zip(self.ordered_model_output, list_output) if pred >= self.threshold]
        else:
            raise("'threshold' must be a float or a list")

    def output_decoding(self, model_output: np.ndarray, confidence: bool = False) -> Dict:
        """Decode the model output.
        Args:
                model_output (np.array): Output of a keras model.
                confidence (bool, optional): Whether or not the model output is returned. The default value is False.
        Returns:
                dict: Dictionary with the desired outputs.
        """

        # Take a list with the output of a keras model with a dense layer as output.
        list_output = model_output[0].tolist()

        if self.decode_output_by == 'argmax':
            output_decoded = self.decode_by_argmax(list_output)
        elif self.decode_output_by == 'threshold':
            # Special case: binary output.
            if len(list_output) == 1:
                output_decoded = self.ordered_model_output[int(
                    np.round(list_output[0]))]
            # Multilabel case: 2+ outputs.
            else:
                output_decoded = self.decode_by_threshold(list_output)

        if confidence:
            return dict(
                output_decoded=output_decoded,
                model_confidence={
                    class_: output for class_, output in zip(self.ordered_model_output, list_output)
                }
            )
        else:
            return dict(
                output_decoded=output_decoded
            )

    def from_json(self, postprocessing_path: str):
        postprocessing_path = Path(postprocessing_path)

        with open(str(postprocessing_path), "r", encoding="utf8") as pp:
            postprocessing = json.load(pp)

        self.ordered_model_output = postprocessing.get("ordered_model_output")
        self.decode_output_by = postprocessing.get("decode_output_by")
        self.threshold = postprocessing.get("threshold")
        self.config = postprocessing
        # print(f"Postprocessing loaded from {postprocessing_path!r}")
