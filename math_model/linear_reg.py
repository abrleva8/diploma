import numpy as np
import pingouin as pg
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline


class LinRegression:
    def __init__(self, data):
        self.data = data

    def train(self):
        X = self.data.iloc[:, :-1]
        y = self.data.iloc[:, -1:]
        return self.sklearn_f(X, y)

    def regression_f(self, predictors, outcome):
        # scaler = StandardScaler()
        # scaler.fit(predictors)
        # predictors_std = scaler.transform(predictors)
        # print(outcome.shape)
        outcome = np.array(outcome).reshape(-1)
        mod = pg.linear_regression(predictors, outcome, relimp=True)
        Y = outcome
        res = mod.residuals_
        df_mod = mod.df_model_  # p
        df_res = mod.df_resid_  # n - p - 1
        SS_mean = sum((Y - np.mean(Y)) ** 2) / (df_res + df_mod)
        SS_res = np.sum(np.square(res)) / (df_res + 1)
        R2 = 1 - ((df_res + 1) * SS_res) / ((df_res + df_mod) * SS_mean)
        F = SS_mean / SS_res
        print(f'F = {F}')
        return F

    def sklearn_f(self, predictors, outcome):
        pipeline = make_pipeline(LinearRegression())
        pipeline.fit(predictors, outcome)
        print(f'R2 = {pipeline.score(predictors, outcome)}')
        y_predict = pipeline.predict(predictors)
        print(f'Среднеквадратичная ошибка = {np.mean((y_predict - outcome) ** 2)}')
        return outcome, y_predict

