import pandas as pd
import pickle

from sklearn.pipeline import Pipeline


class ModelLoader:
    def __init__(self, pipeline: Pipeline, pingouin_result: pd.DataFrame) -> None:
        self.pipeline = pipeline
        self.pingouin_result = pingouin_result

    def save(self, file_name: str) -> None:
        with open(file_name, 'wb') as f:
            pickle.dump(self, f)

    @classmethod
    def read(cls, file_name: str) -> None:
        with open(file_name, 'rb') as f:
            return pickle.load(f)
