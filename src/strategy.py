# Import Dependencies
import technical_analysis as ta
import skyfield as sky

# Import libraries
import pandas as pd
import numpy as np
from datetime import *

Astro = sky.Skyfield()


class Moon_Phase:
    def strategy_MoonPhase(self, symbol, timeInDay, moon_Degrees):
        dataFrame = pd.DataFrame()
        dataFrame["Adj Close"] = symbol["Adj Close"]  # DataFrame
        dataFrame["MoonPhase"] = Astro.get_Moon_Phases_2_Phases(moon_Degrees)
        dataFrame["Regra"] = np.where(dataFrame["MoonPhase"] == "Lua Nova", 1, 0)
        dataFrame["Position"] = (
            dataFrame["Regra"].diff().fillna(0)
        )  # Checka se ouve mudança na regra
        dataFrame["Position"] = np.where(
            dataFrame["Position"].shift(-(1 + timeInDay)) == -1,
            -1,
            dataFrame["Position"],
        )  # Ajusta o dia da venda
        dataFrame["Position"] = np.where(
            dataFrame["Regra"] == 0, 0, dataFrame["Position"]
        )
        dataFrame["Position"] = np.where(
            dataFrame["Position"] == 0, np.nan, dataFrame["Position"]
        )
        dataFrame["Compra"] = np.where(
            dataFrame["Position"] == 1, dataFrame["Adj Close"], np.nan
        )
        dataFrame["Venda"] = np.where(
            dataFrame["Position"] == -1, dataFrame["Adj Close"], np.nan
        )
        dataFrame = dataFrame[~dataFrame["Position"].isna()]
        dataFrame["Venda"] = dataFrame["Venda"].shift(-1)
        dataFrame = dataFrame[~dataFrame["Venda"].isna()]
        dataFrame["Trade"] = (dataFrame["Venda"] - dataFrame["Compra"]) / dataFrame[
            "Compra"
        ]
        dataFrame["Retorno_MP"] = dataFrame["Trade"].cumsum()
        return dataFrame

    def get_Best_Variables(self, base, length, moon_Degrees):
        result = 0
        for x in length:
            aux = self.strategy_MoonPhase(base, x, moon_Degrees).iloc[-1][-1]
            if aux > result:
                melhor_resultado = aux
                melhor_periodo = x
                result = aux
        return melhor_resultado, melhor_periodo

    def strategy_MoonPhase_Annual(self, dataFrame, timeInDay, moon_Degrees):
        dataFrame = self.strategy_MoonPhase(dataFrame, timeInDay, moon_Degrees)

        dateTimeYear1 = []  # Lista com os anos
        for x in dataFrame.index:  # Pega os anos
            date_object = x.year
            dateTimeYear1.append(date_object)

        dataFrame["Year"] = dateTimeYear1  # Adiciona a lista com os anos ao DataFrame
        dataFrame["Year"] = dataFrame["Year"].diff()  # Verifica se o ano mudou
        dataFrame["Year"] = np.where(
            dataFrame["Year"] == 0, np.nan, dataFrame["Year"]
        )  # transforma em nan os anos que não mudaram
        dataFrame["Index"] = dataFrame.reset_index().index  # Indexa o DataFrame
        dataFrame["Annual Index"] = np.where(
            dataFrame["Year"] == 1, dataFrame["Index"], np.nan
        )  # Pega os indices dos anos que mudaram

        Initial_Index = int(
            dataFrame[~dataFrame["Annual Index"].isna()].iloc[0]["Annual Index"] - 1
        )  # Pega o primeiro ano que mudou
        Final_Index = int(
            dataFrame[~dataFrame["Annual Index"].isna()].iloc[-1]["Annual Index"] + 1
        )  # Pega o ultimo ano que mudou
        dataFrame = dataFrame[
            Initial_Index:Final_Index
        ]  # Pega os dados dos anos que mudaram

        dataFrame = dataFrame[~dataFrame["Year"].isna()]  # Pega os anos que mudaram
        dataFrame["Retorno_Alvo"] = dataFrame["Retorno_MP"].shift(
            -1
        )  # Pega o retorno do ano anterior
        dataFrame["Resultado Anual"] = (
            dataFrame["Retorno_Alvo"] - dataFrame["Retorno_MP"]
        )  # Calcula o retorno do ano atual
        dataFrame["Resultado Do Ativo"] = (
            dataFrame["Adj Close"].pct_change(1).shift(-1)
        )  # Calcula o retorno do ativo
        dataFrame = dataFrame[:-1]  # Retira o ano que mudou
        dataFrame = dataFrame.loc[
            :,
            (
                "MoonPhase",
                "Adj Close",
                "Regra",
                "Position",
                "Compra",
                "Venda",
                "Trade",
                "Retorno_MP",
                "Retorno_Alvo",
                "Resultado Anual",
                "Resultado Do Ativo",
            ),
        ]  # Pega as colunas desejadas
        return dataFrame
