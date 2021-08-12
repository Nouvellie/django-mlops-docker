import json

from collections import OrderedDict
from pathlib import Path
from typing import (
    Any,
    List,
    Optional,
    Tuple,
)

FUNCTIONS_PIPELINE = OrderedDict()


def pipeline_function_register(func):
    """Add functions to the pipeline"""

    if func.__name__ not in FUNCTIONS_PIPELINE:
        FUNCTIONS_PIPELINE[func.__name__] = func
        # print(f"{func.__name__} registered in Pipeline")
    else:
        raise Exception(f"Duplicated function with name {func.__name__}")


class Pipeline:
    """
    Build a pipeline of functions
    Pipeline structure: ("func_name", args, kwargs) or ("func_name", kwargs)
    x -> Pipeline(x) -> new_x
    """

    FUNCTIONS_PIPELINE = FUNCTIONS_PIPELINE

    def __new__(cls, pipeline: Optional[List[Tuple[str, dict]]] = None, *args, **kwargs):
        return super(Pipeline, cls).__new__(cls, *args, **kwargs)

    def __init__(self, pipeline: Optional[List[Tuple[str, dict]]] = None):
        self.pipeline = pipeline if pipeline else []

    def __call__(self, model_input: Any,) -> Any:
        """Apply pipeline to the input 'x'."""
        for pipe in self.pipeline:
            func_name, *args, kwargs = pipe
            assert isinstance(kwargs, dict), f"Wrong declaration in {func_name!r}. Must be (str, dict) or (str, tuple, dict)"

            # Apply preprocessing. (args and kwargs provided)
            if args:
                model_input = self.apply(model_input, func_name, *args, **kwargs)
            else:
                model_input = self.apply(model_input, func_name, **kwargs)
        return model_input

    @classmethod
    def apply(cls, model_input: Any, func_name: Any, *args, **kwargs) -> Any:
        """Compute func(x, *args, **kwargs)"""
        if func_name in cls.FUNCTIONS_PIPELINE:
            return cls.FUNCTIONS_PIPELINE[func_name](model_input, *args, **kwargs)
        else:
            raise TypeError(f"{func_name} not available!")

    def from_json(self, preprocessing_path: str):
        preprocessing_path = Path(preprocessing_path)

        with open(str(preprocessing_path), "r", encoding="utf8") as pp:
            pipeline = json.load(pp)

        # TODO: Fix this.
        # Check the availability of the functions.
        # available_functions = {
        #     pipe[0]: self.is_available(pipe[0]) for pipe in pipeline
        # }

        # If all functions are not available.
        # if not all(available_functions.values()):
        # 	not_available_functions = available_functions

        # 	return [func_name for func_name, available in available_functions.items() if available is False]
        self.pipeline = pipeline
        # print("\n", f"Pipeline loaded from {preprocessing_path!r}")

    def is_available(self, func_name: str) -> bool:
        """Return True if the function 'func_name' is available in Pipeline"""
        return True if func_name in self.FUNCTIONS_PIPELINE else False