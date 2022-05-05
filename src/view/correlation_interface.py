# %%
# Import Libraries
import yfinance as yf
import pandas as pd
import sys
import os
from tkinter import *

# Import Dependencies
os.chdir("C:\\Users\\mateu\\Documents\\GitHub\\Data-Science\\src\\controller")
sys.path.append("C:\\Users\\mateu\\Documents\\GitHub\\Data-Science\\src\\controller")

# import data_plot as dp
import data_analysis as da

# %%

LRM = da.LinearRegressionModels()


def correlation(first_asset, second_asset, day):
    """
    It takes two assets and a number of day, downloads the data, calculates the correlation, and
    returns the correlation.

    :param first_asset: The first asset you want to compare
    :param second_asset: The second asset you want to compare to the first asset
    :param day: the number of day to look back
    :return: The correlation between the two assets.
    """

    # Downloading the data from the two assets.
    first_DataFrame = yf.download(first_asset)
    second_DataFrame = yf.download(second_asset)

    # Creating a dataframe with the adjusted close of the two assets.
    adjusted_DataFrame = pd.DataFrame()
    adjusted_DataFrame["first_asset"] = first_DataFrame["Adj Close"]
    adjusted_DataFrame["second_asset"] = second_DataFrame["Adj Close"]

    # dropping the nan values from the dataframe
    adjusted_DataFrame = adjusted_DataFrame[~adjusted_DataFrame["first_asset"].isna()]
    adjusted_DataFrame = adjusted_DataFrame[~adjusted_DataFrame["second_asset"].isna()]

    # Creating two dataframes with the adjusted close of the two assets.
    df1 = pd.DataFrame()
    df1["Close"] = adjusted_DataFrame["first_asset"]

    df2 = pd.DataFrame()
    df2["Close"] = adjusted_DataFrame["second_asset"]

    # Calculating the correlation between the two assets.
    return LRM.correlation(df1, df2, day)


# It creates a window with the title "Ticker Chart".
root = Tk()
root.title("Correlation Chart")


def correlation_input():
    """
    It takes the text from the text boxes, converts the day to an integer, and then sets the button text
    to the correlation of the two assets
    """
    first_asset = first_asset_txt.get("1.0", "end-1c")
    second_asset = second_asset_txt.get("1.0", "end-1c")
    day = int(day_txt.get("1.0", "end-1c"))

    if type(first_asset) == str and type(second_asset) == str and type(day) == int:
        btn_text.set("Correlação: " + str(correlation(first_asset, second_asset, day)))


# Creating a label, a text box, two buttons and setting their properties.
l = Label(text="Correlation")

# It creates a text box with the height of 1, width of 30, and a light yellow background.
first_asset_txt = Text(
    root,
    height=1,
    width=30,
    bg="light yellow",
)

second_asset_txt = Text(
    root,
    height=1,
    width=30,
    bg="light yellow",
)

day_txt = Text(
    root,
    height=1,
    width=30,
    bg="light yellow",
)

# Creating a variable that can be used to change the text of the button.
btn_text = StringVar()

# It creates a button with the height of 1, width of 30, textvariable of btn_text, and the command of
# correlation_input.
correlation_Button = Button(
    root,
    height=1,
    width=30,
    textvariable=btn_text,
    command=lambda: correlation_input(),
)

# It sets the text of the button to "Correlation".
btn_text.set("Correlation")

# The code that creates the GUI.
l.pack()
first_asset_txt.pack()
second_asset_txt.pack()
day_txt.pack()
correlation_Button.pack()
root.mainloop()
