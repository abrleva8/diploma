import pandas as pd


class DataFrameManager:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.__init_columns()

    def get_y(self):
        return self.df[self.df.columns[-1]]

    def get_columns(self):
        return self.df.columns

    def X(self):
        return self.df.drop(self.df.columns[-1], axis=1)

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

    @staticmethod
    def get_conditions(df: pd.DataFrame) -> pd.DataFrame:
        df_conditions = df[['номер_опыта', 'материал', 'условие', 'значение_условия']]

        new_columns = df_conditions['условие'].value_counts().keys()

        for key in new_columns:
            df_conditions[key] = df_conditions[df_conditions['условие'] == key]['значение_условия']

        total_columns = ['номер_опыта', 'материал']
        total_columns.extend(new_columns)
        df_conditions = df_conditions[total_columns]
        return df_conditions

    @staticmethod
    def get_results(df: pd.DataFrame) -> pd.DataFrame:
        df_res = df[['номер_опыта', 'материал', 'имя_результат', 'результат_эксперимента']]
        new_columns = df_res['имя_результат'].value_counts().keys()

        for key in new_columns:
            df_res[key] = df_res[df_res['имя_результат'] == key]['результат_эксперимента']

        total_columns = ['номер_опыта', 'материал']
        total_columns.extend(new_columns)
        df_res = df_res[total_columns]
        df_result = pd.pivot_table(df_res, index=['номер_опыта', 'материал']).reset_index()
        return df_result

    @staticmethod
    def get_research_df(df):
        df_conditions = DataFrameManager.get_conditions(df)
        df_result = DataFrameManager.get_results(df)

        df_total = pd.merge(df_conditions, df_result, on='номер_опыта', suffixes=('', '_y'))
        df_total = df_total.drop_duplicates()
        return df_total
