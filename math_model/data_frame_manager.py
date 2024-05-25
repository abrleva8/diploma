import pandas as pd


class DataFrameManager:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.__init_columns()

    def get_y(self):
        return self.df[self.df.columns[-1]]

    def save_df(self, filename: str):
        self.df = self.df.rename(columns=self.new_columns)
        self.df.to_csv(filename, index=False)
        self.df = self.df.rename(columns=self.old_columns)

    def __init_columns(self):
        columns = self.df.columns
        self.new_columns = {column: column.split(',')[0] for column in columns}
        self.old_columns = {column.split(',')[0]: column for column in self.new_columns.keys()}

    def rename_dict(self) -> dict:
        new_columns = []
        for (index, a) in self.df.iterrows():
            res = ': '.join([a[column] for column in self.df.columns])
            new_columns.append(res)
        return dict(zip(self.df['name'], new_columns))
