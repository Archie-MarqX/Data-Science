# %%
import datetime
import time as t
from shared import Util
from skyfield.api import *
from skyfield.framelib import *
from skyfield import almanac
from skyfield import api

# %%

get_Percent = Util.Util().get_Percent
show_Percent = Util.Util().show_Percent

class Skyfield:
    date = datetime.utcnow()
    reference_Datetime = date.year, date.month, date.day, date.hour, date.minute

    def set_Datetime(self, date, GMT=0):
        self.reference_Datetime = (
            date.year,
            date.month,
            date.day,
            date.hour + -GMT,
            date.minute,
        )
        return self

    def set_latlong(self, latitude, longitude):
        latlong = latitude, longitude
        return latlong

    def get_Moon_Phase(self):
        ts = load.timescale()
        eph = api.load("de421.bsp")
        t = ts.utc(*self.reference_Datetime)
        phase = almanac.moon_phase(eph, t)
        return phase.degrees

    def get_Planet_Phase(self, lat=42.21 * N, long=-71.03 * W, planet="mars"):
        ts = load.timescale()
        t = ts.utc(*self.reference_Datetime)

        eph = load("de421.bsp")
        sun, Planet, earth = eph["sun"], eph[planet], eph["earth"]
        city = earth + wgs84.latlon(lat, long)

        c = city.at(t)
        _, m, _ = c.observe(Planet).apparent().frame_latlon(ecliptic_frame)
        _, s, _ = c.observe(sun).apparent().frame_latlon(ecliptic_frame)
        phase = (m.degrees - s.degrees) % 360.0

        return phase

    # Refatorar o código
    def get_Moon_Degree(self, yf_Dataframe):  # get moon degree based on Dataframe index
        dateTime = []
        dataFrame_Length = len(yf_Dataframe)

        for element in yf_Dataframe.index:
            dateTime.append(element)

        PT1 = int((len(dateTime) - 1) * 0.25)
        PT2 = int((len(dateTime) - 1) * 0.5)
        PT3 = int((len(dateTime) - 1) * 0.75)
        PT4 = int((len(dateTime) - 1) * 1)

        first_Quarter = dateTime[:PT1]
        second_Quarter = dateTime[PT1:PT2]
        third_Quarter = dateTime[PT2:PT3]
        last_Quarter = dateTime[PT3:]

        moon_Degree = []
        start = t.time()

        print("Loop de Atribuição iniciado")
        for element in first_Quarter:
            moon = self.set_Datetime(element).get_Moon_Phase()
            moon_Degree.append(moon)

        first_Quarter_Time = t.time()
        print(show_Percent(get_Percent(PT1, dataFrame_Length))+" concluido")
        print(len(moon_Degree))
        print(str(first_Quarter_Time - start) + "\n")

        for element in second_Quarter:
            moon = self.set_Datetime(element).get_Moon_Phase()
            moon_Degree.append(moon)

        second_Quarter_Time = t.time()
        print(show_Percent(get_Percent(PT2, dataFrame_Length))+" concluido")
        print(len(moon_Degree))
        print(str(second_Quarter_Time - first_Quarter_Time) + "\n")

        for element in third_Quarter:
            moon = self.set_Datetime(element).get_Moon_Phase()
            moon_Degree.append(moon)

        third_Quarter_Time = t.time()
        print(show_Percent(get_Percent(PT3, dataFrame_Length))+" concluido")
        print(len(moon_Degree))
        print(str(third_Quarter_Time - second_Quarter_Time) + "\n")

        for element in last_Quarter:
            moon = self.set_Datetime(element).get_Moon_Phase()
            moon_Degree.append(moon)

        print(show_Percent(get_Percent(PT4, dataFrame_Length))+" concluido")
        print(len(moon_Degree))
        print(str(t.time() - third_Quarter_Time) + "\n")

        print("Duration: " + str(t.time() - start))
        return moon_Degree

    def get_Moon_Phases_(self, moon_Degree):
        moon_Phases = []

        for element in moon_Degree:
            if element < 90:
                moon_Phases.append("Lua Nova")
            if element >= 90 and element < 180:
                moon_Phases.append("Lua Crescente")
            if element >= 180 and element < 270:
                moon_Phases.append("Lua Cheia")
            if element >= 270 and element < 360:
                moon_Phases.append("Lua Minguante")
            if element >= 360:
                moon_Phases.append("Lua Nova")

        return moon_Phases

    # %%

    def get_Moon_Phases_2_Phases(self, moon_Degree):
        moon_Phases = []

        for element in moon_Degree:
            if element < 180:
                moon_Phases.append("Lua Nova")
            if element >= 180 and element < 360:
                moon_Phases.append("Lua Cheia")
            if element >= 360:
                moon_Phases.append("Lua Nova")

        return moon_Phases
