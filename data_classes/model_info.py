import pandas as pd

from dataclasses import dataclass


@dataclass
class ModelInfo:
    pingouin_result: pd.DataFrame
    fisher_result: float
    fisher_table: pd.DataFrame
    r2: float
    mse: float
