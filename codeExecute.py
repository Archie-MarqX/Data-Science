# %%
import technicalAnalysis  as ta
import binanceAPI as bAPIfunc
import json
from datetime import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from skyfield.api import load
from skyfield.framelib import ecliptic_frame

# %%
# Generate keys or load them
try:
    with open('keys.json', 'r') as f:
        keys = json.load(f)
except:
    keys = [
        input('API_KEY: '),
        input('SECRET_KEY: ')
    ]
    with open('keys.json', 'w', encoding='utf-8') as f:
        json.dump(keys, f, ensure_ascii=False, indent=4)
    print('Keys Generated')

# Set Keys
API_KEY     = keys[0]
SECRET_KEY  = keys[1]

spot_bapi = bAPIfunc.spot_Kline(API_KEY,SECRET_KEY)

spot_120m_CandleValues  = pd.read_csv('spot_120m_Candles.csv')
spot_Daily_CandleValues = pd.read_csv('spot_dailyCandles.csv')

date = ta.Date()
Astro   = ta.Astronomy_Skyfield()
dateTime = []

# %%
for x in spot_Daily_CandleValues['TimeOpen']:
    dateTime.append(date.get_date(x))


moonType = []

for x in dateTime:
    moon = Astro.setDatetime(x).getMoonPhase()
    moonType.append(moon)

moonPhases = []

for x in moonType:
    if x < 90:
        moonPhases.append('Lua Nova')
    if x >= 90 and x < 180:
        moonPhases.append('Lua Crescente')
    if x >= 180 and x < 270:
        moonPhases.append('Lua Cheia')
    if x >= 270 and x < 360:
        moonPhases.append('Lua Minguante')
    if x >= 360:
        moonPhases.append('Lua Nova')

index = 0
moonPhasesIndex = len(moonPhases)

moonPhasesCycle = []

for x in moonPhases:
    index += 1
    if index < moonPhasesIndex:
        if moonPhases[index-1] != moonPhases[index]:
            moonPhasesCycle.append(moonPhases[index])
        else:
            moonPhasesCycle.append(np.nan)

df_MoonPhases = pd.DataFrame()
df_MoonPhases['MoonPhase'] = moonPhasesCycle
df_MoonPhases['Ativo'] = spot_Daily_CandleValues['Close']

# %%
def regra(base):
    preco_compra = []
    preco_venda = []
    aux = 0
    for i in range(len(base)):
        if base['MoonPhase'][i] == 'Lua Nova':
            if aux != 1:
                preco_compra.append(base['Ativo'][i])
                preco_venda.append(np.nan)
                aux = 1
            else:
                preco_compra.append(np.nan)
                preco_venda.append(np.nan)
        elif base['MoonPhase'][i] == 'Lua Cheia':
            if aux != 0:
                preco_compra.append(np.nan)
                preco_venda.append(base['Ativo'][i])
                aux = 0
            else:
                preco_compra.append(np.nan)
                preco_venda.append(np.nan)
        else:
            preco_compra.append(np.nan)
            preco_venda.append(np.nan)
    
    return (preco_compra, preco_venda)

compra,venda = regra(df_MoonPhases)

sinal = pd.DataFrame()
sinal["Compra"] = compra
sinal["Venda"] = venda
df_MoonPhases["Compra"] = compra
df_MoonPhases["Venda"] = venda

df_regra = df_MoonPhases

# %%
plt.figure(figsize = (16, 10))
plt.plot(df_regra["Ativo"], label = "Ativo", alpha = 0.75, linewidth = 2, color = "blue")
plt.scatter(df_regra.index, df_regra["Compra"]*0.95, label = "Compra", marker = "^", s = 100, color = "green")
plt.scatter(df_regra.index, df_regra["Venda"]*1.05, label = "Venda", marker = "v", s = 100, color = "red")
plt.title("Regra de trade - Cruzamento de Médias")
plt.legend(loc = "lower right")
plt.xlabel("2017 à 2022")
plt.ylabel("Cotação")
plt.show()

# %%
df_compra = df_regra[ ~ df_regra["Compra"].isna()]
np.array(df_compra["Compra"])
df_venda = df_regra[ ~ df_regra["Venda"].isna()]
np.array(df_venda["Venda"])

Compra  = df_regra['Compra'].dropna(axis=0).values.tolist()
Venda   = df_regra['Venda'].dropna(axis=0).values.tolist()


df = pd.DataFrame()
df['Compra']    = Compra
df['Venda']     = Venda

# %%
Trade = []
for x in df:
    Trade.append(df['Venda'] - df['Compra'])

df['Trade'] = Trade[0]

resultado = [0]
index = -1
for x in df['Trade']:
    index += 1
    resultado.append(resultado[index] + x)

df['Resultado'] = resultado[-(len(resultado)-1):]

# %%

plt.figure(figsize = (16, 10))
plt.plot(df["Resultado"], label = "Ativo", alpha = 0.75, linewidth = 2, color = "blue")
plt.hlines(0,0,max(df.index.values))
plt.vlines(df['Resultado'].idxmax(),0,df['Resultado'].max())
plt.title("Regra de trade - Fases da Lua")
plt.legend(loc = "lower right")
plt.xlabel("2017 à 2022")
plt.ylabel("Cotação")
plt.show()