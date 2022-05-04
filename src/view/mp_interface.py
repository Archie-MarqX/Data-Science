# Import Dependencies
from controller import technical_analysis as ta
from controller import astronomy as sky
from controller import data_plot as dp
from controller import strategy as st

# Import Libraries
import yfinance as yf
from tkinter import *

# Creating an object of the class Skyfield, DataPlot and Moon_Phase.
Astro = sky.Skyfield()
plot = dp.DataPlot()
strategy = st.Moon_Phase()


def Moon_Phase_Strategy(ticker):
    """
    It downloads the stock data from Yahoo Finance, gets the moon degree based on the DataFrame index,
    gets the best variables, gets the moon phase DataFrame with best variables and strategy return, sets
    the DataPlotConfig object, plots the DataFrame, gets the mean return and standard deviation of the
    return
    
    :param ticker: The ticker symbol of the stock you want to analyze
    """
    yahoo_DataFrame = yf.download(ticker)

    moon_Degree = Astro.get_Moon_Phase(
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

    mean_Return = moon_Phase_DataFrame["Retorno_MP"].mean()  # mean return
    std_Return = moon_Phase_DataFrame["Retorno_MP"].std()  # standard deviation of the return

    print("Média De Retorno: " + str(mean_Return))
    print("Média De Desvio Padrão: " + str(std_Return))


def Asset_Return(ticker):
    """
    It downloads the data from Yahoo Finance, calculates the asset return, removes the first row (which
    is NaN) and plots the asset return
    
    :param ticker: The ticker of the asset you want to download
    :return: A DataFrame with the asset return.
    """
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


# It creates a window with the title "Ticker Chart".
root = Tk()
root.title("Ticker Chart")


def MP_Input():
    """
    It takes the input from the text box and passes it to the Moon_Phase_Strategy function.
    """
    INPUT = inputtxt.get("1.0", "end-1c")
    if type(INPUT) == str:
        Moon_Phase_Strategy(INPUT)


def Asset_Input():
    """
    It takes the input from the text box and passes it to the Asset_Return function.
    """
    INPUT = inputtxt.get("1.0", "end-1c")
    if type(INPUT) == str:
        Asset_Return(INPUT)


# Creating a label, a text box, two buttons and setting their properties.
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

# The code that creates the GUI.
l.pack()
inputtxt.pack()
mp_Button.pack()
asset_Button.pack()
root.mainloop()

# %%
