import pandas as pd
import joblib

from sklearn.pipeline import Pipeline


class ModelLoader:
    def __init__(self, pipeline: Pipeline, pingouin_result: pd.DataFrame) -> None:
        self.pipeline = pipeline
        self.pingouin_result = pingouin_result

    def save(self, file_name: str) -> None:
        joblib.dump(self, file_name)

    @classmethod
    def read(cls, file_name: str) -> None:
        pass
