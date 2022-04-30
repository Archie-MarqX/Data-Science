# Import libraries
import  pandas  as pd
import  time    as t
from    datetime            import *
from    skyfield.api        import *
from    skyfield.framelib   import *
from    skyfield            import almanac
from    skyfield            import api

# Data
class Date:
    def get_date(self,Unix):
        get_Date = datetime.utcfromtimestamp(Unix / 1000)
        return get_Date
    
    def get_unix(self,Date):
        get_Unix = time.mktime(datetime.timetuple(Date))
        return get_Unix
    
    def get_datetime(self,time):
        get_datetime = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
        return get_datetime

class CSV:
    def getCSV(self,dataFrame, fileName):
        dataFrame.to_csv(fileName, index=False,  encoding='utf-8')

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
        return phase.degrees

    def getPlanetPhase(self, lat = 42.21 * N, long= -71.03 * W, planet='mars'): 
        ts = load.timescale()
        t = ts.utc(*self.referenceDatetime)

        eph = load('de421.bsp')
        sun, Planet, earth = eph['sun'], eph[planet], eph['earth']
        city = earth + wgs84.latlon(lat, long)

        c = city.at(t)
        _, m, _ = c.observe(Planet).apparent().frame_latlon(ecliptic_frame)
        _, s, _ = c.observe(sun).apparent().frame_latlon(ecliptic_frame)
        phase = (m.degrees - s.degrees) % 360.0

        return phase

# Refatorar o código
    def getMoon_Degree(self,yf_Dataframe): #get moon degree based on Dataframe index
        dateTime = []

        for x in yf_Dataframe.index:
            dateTime.append(x)

        PT1 = int((len(dateTime)-1) * 0.25)
        PT2 = int((len(dateTime)-1) * 0.5)
        PT3 = int((len(dateTime)-1) * 0.75)
        PT4 = int((len(dateTime)-1) * 1)

        X = dateTime[:PT1]
        Y = dateTime[PT1:PT2]
        Z = dateTime[PT2:PT3]
        W = dateTime[PT3:]

        moonType = []
        start = t.time()

        print("Loop de Atribuição iniciado")
        for x in X:
            moon = self.setDatetime(x).getMoonPhase()
            moonType.append(moon)

        PT1 = t.time()
        print('25% Concluido')
        print(len(moonType))
        print(str(PT1 - start)+'\n')

        for x in Y:
            moon = self.setDatetime(x).getMoonPhase()
            moonType.append(moon)

        PT2 = t.time()
        print('50% Concluido')
        print(len(moonType))
        print(str(PT2 - PT1)+'\n')

        for x in Z:
            moon = self.setDatetime(x).getMoonPhase()
            moonType.append(moon)

        PT3 = t.time()
        print('75% Concluido')
        print(len(moonType))
        print(str(PT3 - PT2)+'\n')

        for x in W:
            moon = self.setDatetime(x).getMoonPhase()
            moonType.append(moon)

        PT4 = t.time()
        print('100% Concluido')
        print(len(moonType))
        print(str(PT4 - PT3)+'\n')

        print("Duration: "+str(PT4 - start))
        return moonType

    def getMoon_Phases(self,moon_Degree):
        moonPhases = []

        for x in moon_Degree:
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

        return moonPhases

# %%

    def getMoon_Phases_2_Phases(self,moon_Degree):
        moonPhases = []

        for x in moon_Degree:
            if x < 180:
                moonPhases.append('Lua Nova')
            if x >= 180 and x < 360:
                moonPhases.append('Lua Cheia')
            if x >= 360:
                moonPhases.append('Lua Nova')

        return moonPhases
