import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression


class LinearRegressionModels:
    def rsquared(self, x, y):
        xArray = np.array(x).reshape((-1, 1))
        yArray = np.array(y).reshape((-1, 1))

        model = LinearRegression().fit(xArray, yArray)
        r_sq = model.score(xArray, yArray)
        return r_sq

    def correlation(self, firstAsset_DataFrame, secondAsset_DataFrame,total_days=1000):

        first_DataFrame = pd.DataFrame()
        first_DataFrame["Close"] = firstAsset_DataFrame["Close"]
        first_DataFrame = first_DataFrame[-total_days:]
        first_DataFrame["Lagged Close"] = first_DataFrame["Close"].shift(-1)
        first_DataFrame["LN"] = np.log(
            first_DataFrame["Close"] / first_DataFrame["Lagged Close"]
        )
        first_DataFrame = first_DataFrame[~first_DataFrame["Lagged Close"].isna()]

        second_DataFrame = pd.DataFrame()
        second_DataFrame["Close"] = secondAsset_DataFrame["Close"]
        second_DataFrame = second_DataFrame[-total_days:]
        second_DataFrame["Lagged Close"] = second_DataFrame["Close"].shift(-1)
        second_DataFrame["LN"] = np.log(
            second_DataFrame["Close"] / second_DataFrame["Lagged Close"]
        )
        second_DataFrame = second_DataFrame[~second_DataFrame["Lagged Close"].isna()]

        return self.rsquared(first_DataFrame["LN"], second_DataFrame["LN"])
