import pandas as pd


class DataFrameManager:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def get_y(self):
        return self.df[self.df.columns[-1]]

    def save_df(self, filename: str):
        self.df.to_csv(filename, index=False)

    # @property
    # def df(self) -> pd.DataFrame:
    #     return self.df
    #
    # @df.setter
    # def df(self, value: pd.DataFrame):
    #     self.__df = value

