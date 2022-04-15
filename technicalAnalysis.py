import pandas as pd
from datetime import *
import time

# Data
class Date:
    def get_date(self,Unix):
        get_Date = datetime.fromtimestamp(Unix / 1000)
        return get_Date
    
    def get_unix(self,Date):
        get_Unix = time.mktime(datetime.timetuple(Date))
        return get_Unix
    
    def get_datetime(self,time):
        get_datetime = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
        return get_datetime

# Indicadores
class indicators:
    def sma(self,source, length):
        sma = source.rolling(length).mean()
        return sma.dropna(axis=0)
    
    def ema(self,source, periods):
        sma = source.rolling(window=periods, min_periods=periods).mean()[:periods]
        rest = source[periods:]
        return pd.concat([sma, rest]).ewm(span=periods, adjust=False).mean().dropna(axis=0)

    def CCI(self, source, length): 
        df = pd.DataFrame()
        df['TP'] = source
        df['sma'] = df['TP'].rolling(length).mean()
        df['mad'] = df['TP'].rolling(length).apply(lambda x: pd.Series(x).mad())
        df['CCI'] = (df['TP'] - df['sma']) / (0.015 * df['mad'])
        return df['CCI'].dropna(axis=0)
    
    def MACD(self, source, fast_length, slow_length, signal_length):
        MACD = self.ema(source, fast_length) - self.ema(source, slow_length)
        df = pd.DataFrame()
        df['MACD'] = pd.DataFrame(MACD).dropna(axis=0)
        macdSignal = pd.DataFrame()
        macdSignal['MACD'] = df['MACD']
        macdSignal['MACD_Signal'] = self.ema(macdSignal['MACD'],signal_length)
        macdSignal['Histogram'] = macdSignal['MACD'] - macdSignal['MACD_Signal']
        return macdSignal['Histogram']

class Astronomy:
    class MoonPhase:
        date = datetime.today()

        def setDate(self, date):
            self.date = date
            return self

        def calculateDaysIntoCycle(self,date):
            year =  date.year
            month = date.month
            day =   date.day
            A = int(year / 100)
            B = int(A / 4)
            C = 2 - A + B
            E = int(365.25 * (year + 4716))
            F = int(30.6001 * (month + 1))
            JD = C + day + E + F - 1524.5
            daysSinceNew = JD - 2451549.5
            newMoons = daysSinceNew / 29.53
            daysIntoCycle = (newMoons - int(newMoons)) * 29.53
            return daysIntoCycle

        def getCurrentMoonPhase(self,daysIntoCycle):
            if (daysIntoCycle < 7):
                return 'Lua Nova'
            elif(daysIntoCycle >= 7 and daysIntoCycle < 15):
                return 'Quarto Crescente'
            elif(daysIntoCycle >= 15 and daysIntoCycle < 22):
                return 'Lua Cheia'
            elif(daysIntoCycle >= 22 and daysIntoCycle < 29):
                return 'Quarto Minguante '
            elif(daysIntoCycle >= 29.5):
                return 'Lua Nova'

        def getMoonPhase(self):
            daysIntoCycle = self.calculateDaysIntoCycle(self.date)
            currentMoonPhase = self.getCurrentMoonPhase(daysIntoCycle)
            daysIntoCycle = round(daysIntoCycle, 2)
            return daysIntoCycle, currentMoonPhase

        def printMoonPhase(self):
            print(self.getMoonPhase())
            return self
