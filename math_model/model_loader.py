from __future__ import annotations

import pandas as pd
import joblib

from sklearn.pipeline import Pipeline

from data_classes.model_info import ModelInfo


class ModelLoader:
    def __init__(self, pipeline: Pipeline = None, model_info: ModelInfo = None) -> None:
        self.pipeline = pipeline
        self.model_info = model_info

    def save(self, file_name: str) -> None:
        joblib.dump(self, file_name)

    @classmethod
    def load(cls, file_name: str) -> ModelLoader:
        model_loader = joblib.load(file_name)

        assert isinstance(model_loader, ModelLoader)

        return model_loader
