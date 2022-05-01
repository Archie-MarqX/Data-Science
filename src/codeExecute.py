# Import Dependencies
import technicalAnalysis as ta
import Skyfield as sky
import dataPlot as dp
import strategy as st

# Import Libraries
import yfinance as yf

ticker = "BTC-USD"
yahoo_DataFrame = yf.download(ticker)


Astro = sky.Skyfield()
plot = dp.DataPlot()
strategy = st.Moon_Phase()


moon_Degree = Astro.get_Moon_Degree(
    yahoo_DataFrame
)  # get moon degree based on Dataframe index

_, period = strategy.get_Best_Variables(
    yahoo_DataFrame, range(0, 7, 1), moon_Degree
)  # get best variables

moon_Phase_DataFrame = strategy.strategy_MoonPhase(yahoo_DataFrame, period, moon_Degree)

config = (
    plot.DataPlotConfig()
    .set_Axis_X_Name("Data")
    .set_Axis_Y_Name("Retorno em %")
    .set_Title(ticker)
    .set_dataFrame(moon_Phase_DataFrame["Retorno_MP"])
)

plot.simple_Plot(config)


mean_Return = moon_Phase_DataFrame["Retorno_MP"].mean()  # media de retorno
std_Return = moon_Phase_DataFrame["Retorno_MP"].std()  # desvio padrão do retorno

print("Média De Retorno: " + str(mean_Return))
print("Média De Desvio Padrão: " + str(std_Return))
