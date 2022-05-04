# Import Dependencies
import technical_analysis as ta
import astronomy as sky
import data_plot as dp
import strategy as st

# Import Libraries
import yfinance as yf
from tkinter import *

Astro = sky.Skyfield()
plot = dp.DataPlot()
strategy = st.Moon_Phase()


def Moon_Phase_Strategy(ticker):
    yahoo_DataFrame = yf.download(ticker)

    moon_Degree = Astro.get_Moon_Degree(
        yahoo_DataFrame
    )  # get moon degree based on Dataframe index

    _, period = strategy.get_Best_Variables(
        yahoo_DataFrame,
        range(0, 7, 1),
        moon_Degree,
    )  # get best variables

    # get moon phase DataFrame with best variables and strategy return
    moon_Phase_DataFrame = strategy.strategy_MoonPhase(
        yahoo_DataFrame,
        period,
        moon_Degree,
    )

    config = (
        plot.DataPlotConfig()
        .set_Axis_X_Name("Data")
        .set_Axis_Y_Name("Retorno em %")
        .set_Title(ticker)
        .set_dataFrame(moon_Phase_DataFrame["Retorno_MP"])
    )  # set DataPlotConfig object

    # plot.simple_Plot(config)  # plot DataFrame
    plot.simple_Plot(config)

    mean_Return = moon_Phase_DataFrame["Retorno_MP"].mean()  # media de retorno
    std_Return = moon_Phase_DataFrame["Retorno_MP"].std()  # desvio padrão do retorno

    print("Média De Retorno: " + str(mean_Return))
    print("Média De Desvio Padrão: " + str(std_Return))


def Asset_Return(ticker):
    yahoo_DataFrame = yf.download(ticker)
    yahoo_DataFrame["Asset Return"] = (
        yahoo_DataFrame["Adj Close"].pct_change(1).shift(-1).cumsum()
    )
    yahoo_DataFrame = yahoo_DataFrame[~yahoo_DataFrame["Asset Return"].isna()]

    config = (
        plot.DataPlotConfig()
        .set_Axis_X_Name("Data")
        .set_Axis_Y_Name("Retorno em %")
        .set_Title(ticker)
        .set_dataFrame(yahoo_DataFrame["Asset Return"])
    )  # set DataPlotConfig object

    plot.simple_Plot(config)

    return yahoo_DataFrame


root = Tk()
root.title("Ticker Chart")


def MP_Input():
    INPUT = inputtxt.get("1.0", "end-1c")
    if type(INPUT) == str:
        Moon_Phase_Strategy(INPUT)


def Asset_Input():
    INPUT = inputtxt.get("1.0", "end-1c")
    if type(INPUT) == str:
        Asset_Return(INPUT)


l = Label(text="Ticker")
inputtxt = Text(
    root,
    height=1,
    width=30,
    bg="light yellow",
)

mp_Button = Button(
    root,
    height=1,
    width=30,
    text="Show Moon Phase Chart",
    command=lambda: MP_Input(),
)

asset_Button = Button(
    root,
    height=1,
    width=30,
    text="Show Asset Return Chart",
    command=lambda: Asset_Input(),
)

l.pack()
inputtxt.pack()
mp_Button.pack()
asset_Button.pack()
root.mainloop()

# %%
