import pandas as pd

from sklearn.base import BaseEstimator, TransformerMixin


class CustomTransformer(BaseEstimator, TransformerMixin):

    def __init__(self, column_names: list, text: str):
        self.column_names = column_names
        self.text = text

    def fit(self, X: pd.DataFrame, y=None):
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        X_transformed = self.__get_new_x(X, self.text)

        return X_transformed

    @classmethod
    def __drop_a(cls, mult: str) -> str:
        ind = mult.find('*')
        if ind != -1:
            mult = mult[ind + 1:]
        else:
            mult = ''
        return mult

    @classmethod
    def __drop_y(cls, mult: str) -> str:
        if mult[0] == 'y':
            mult = '*'.join(mult.split('=')[1:]).strip()
        return mult

    def __get_new_columns(self, df: pd.DataFrame, text: str) -> tuple[list[str], dict]:
        new_columns = df.columns[2:].str.split(', ')

        d = {}
        print(new_columns)
        for column in new_columns:
            d[column[1]] = column[0] + ', ' + column[1]

        text = self.__drop_y(text)

        new_keys = list(map(self.__drop_a, text.split('+')))
        new_keys = list(filter(lambda x: bool(x), new_keys))

        return new_keys, d

    def __get_new_x(self, df: pd.DataFrame, text: str) -> pd.DataFrame:

        new_keys, d = self.__get_new_columns(df, text)
        new_X = pd.DataFrame()

        for key in new_keys:
            if d.get(key, None) in df.columns:
                new_X[key] = df[d[key]]
            else:
                x = key.split('*')
                # print(new_X)
                new_X[key] = df[d[x[0].strip()]] * df[d[x[1].strip()]]
        # print(new_X)
        return new_X
