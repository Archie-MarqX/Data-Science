import technicalAnalysis  as ta
import binanceAPI as bAPIfunc
import json
from datetime import *
import pandas as pd
import numpy as np
from skyfield.api import load
from skyfield.framelib import ecliptic_frame

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

# candles = spot_bapi.get_AllKlines("1D", 86400000,)
# candlesList = ta.attr_loop(candles)
# candleValue = pd.DataFrame(candlesList)
# candleValue.to_csv('spot_dailyCandles', encoding='utf-8', index=False)

spot_120m_CandleValues  = pd.read_csv('spot_120m_Candles.csv')
spot_Daily_CandleValues = pd.read_csv('spot_dailyCandles.csv')

date = ta.Date()
dateTime = []

for x in spot_Daily_CandleValues['TimeOpen']:
    dateTime.append(date.get_date(x))

Astro   = ta.Astronomy_Skyfield()

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
# moonType = []

# for x in spot_Daily_CandleValues['Datetime']:
#     moon = MP.setDate(x).getMoonPhase()
#     moonType.append(moon)

# spot_Daily_CandleValues['MoonPhase'] = moonType

# df_MoonPhase = spot_Daily_CandleValues['MoonPhase']

# fullMoon = []

# for x in df_MoonPhase:
#     if x == 'Lua Cheia':
#         fullMoon.append(x)
#     else:
#         fullMoon.append(np.nan)

# newMoon = []

# for x in df_MoonPhase:
#     if x == 'Lua Nova':
#         newMoon.append(x)
#     else:
#         newMoon.append(np.nan)

# df_MoonPhases = pd.DataFrame()
# df_MoonPhases['fullMoon']   = fullMoon
# df_MoonPhases['newMoon']    = newMoon