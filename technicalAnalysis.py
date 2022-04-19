import pandas as pd
from datetime import *
import time
from skyfield.api import *
from skyfield.framelib import *
from skyfield import almanac
from skyfield import api

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
        SynodicPeriod   = 29.530589

        def setDate(self, date):
            self.date   = date
            return self

        def calculateDaysIntoCycle(self,date):
            year            = date.year
            month           = date.month
            day             = date.day
            A               = int(year / 100)
            B               = int(A / 4)
            C               = 2 - A + B
            E               = int(365.25 * (year + 4716))
            F               = int(30.6001 * (month + 1))
            JD              = C + day + E + F - 1524.5
            daysSinceNew    = JD - 2451549.5
            newMoons        = daysSinceNew / self.SynodicPeriod
            daysIntoCycle   = (newMoons - int(newMoons)) * self.SynodicPeriod
            return daysIntoCycle

        def getCurrentMoonPhase(self,daysIntoCycle):
            FirstQuarter    = self.SynodicPeriod * 0.25
            SecondQuarter   = self.SynodicPeriod * 0.5
            ThirdQuarter    = self.SynodicPeriod * 0.75
            LastQuarter     = self.SynodicPeriod

            if (daysIntoCycle < FirstQuarter):
                return 'Lua Nova'
            elif(daysIntoCycle >= FirstQuarter and daysIntoCycle < SecondQuarter):
                return 'Quarto Crescente'
            elif(daysIntoCycle >= SecondQuarter and daysIntoCycle < ThirdQuarter):
                return 'Lua Cheia'
            elif(daysIntoCycle >= ThirdQuarter and daysIntoCycle < LastQuarter):
                return 'Quarto Minguante '
            elif(daysIntoCycle >= LastQuarter):
                return 'Lua Nova'

        def getMoonPhase(self):
            daysIntoCycle       = self.calculateDaysIntoCycle(self.date)
            currentMoonPhase    = self.getCurrentMoonPhase(daysIntoCycle)
            daysIntoCycle       = round(daysIntoCycle, 2)
            return daysIntoCycle, currentMoonPhase

        def printMoonPhase(self):
            print(self.getMoonPhase())
            return self

class Astronomy_Skyfield:
    date = datetime.utcnow()
    referenceDatetime = date.year,date.month,date.day, date.hour, date.minute

    def setDatetime(self,date,GMT=0):
        self.referenceDatetime  = date.year,date.month,date.day, date.hour + -GMT, date.minute
        return self

    def setlatlong(self,latitude,longitude):
        latlong = latitude, longitude
        return latlong

    def getMoonPhase(self):
        ts = load.timescale()
        eph = api.load('de421.bsp')
        t = ts.utc(*self.referenceDatetime)
        phase = almanac.moon_phase(eph, t)
        return ('Moon phase: {:.1f} degrees'.format(phase.degrees))

    def getPlanetPhase(self, lat = 42.21 * N, long= -71.03 * W, planet='mars'): 
        ts = load.timescale()
        t = ts.utc(*self.dateParams)

        eph = load('de421.bsp')
        sun, Planet, earth = eph['sun'], eph[planet], eph['earth']
        city = earth + wgs84.latlon(lat, long)

        c = city.at(t)
        _, m, _ = c.observe(Planet).apparent().frame_latlon(ecliptic_frame)
        _, s, _ = c.observe(sun).apparent().frame_latlon(ecliptic_frame)
        phase = (m.degrees - s.degrees) % 360.0

        return ('{0:.1f}'.format(phase))