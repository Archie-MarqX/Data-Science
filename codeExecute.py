# %%
# Import Dependencies 
import technicalAnalysis    as  ta
import dataPlot             as  dp
import strategy             as  st

# Import Libraries
import yfinance             as  yf

# %%
ticker  = 'BTC-USD'

df      = yf.download(ticker)

date        = ta.Date()
Astro       = ta.Astronomy_Skyfield()
plot        = dp.DataPlot()
strategy    = st.MoonPhase()

# %%
moonDegree  = Astro.getMoon_Degree(df)

# %%
_, period =  strategy.getBestVariables(df, range(0, 7, 1), moonDegree)

# %%
df1 = strategy.strategy_MoonPhase(df, period, moonDegree)

# %%
dfBase  = df1['Retorno_MP']
eixoX = 'Data'
eixoY = 'Retorno em %'

plot.simplePlot(dfBase, ticker, eixoX, eixoY)
plot.simplePlot(df['Adj Close'].pct_change(1).shift(-1).cumsum(), ticker, eixoX, eixoY)
