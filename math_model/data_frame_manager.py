import pandas as pd


class DataFrameManager:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    # @property
    # def df(self) -> pd.DataFrame:
    #     return self.df
    #
    # @df.setter
    # def df(self, value: pd.DataFrame):
    #     self.__df = value

